from skimage.measure import label, regionprops
from grid_utils import crop_it
from scipy import ndimage
import numpy as np

##################### Milestones AB #####################
four_way = np.array([[0, 1, 0],
                     [1, 1, 1],
                     [0, 1, 0]],
                    dtype=np.uint8,)
three_ex_three = np.ones((3, 3), dtype=bool)

def rule_mirror(grid: np.ndarray):

    h, _ = grid.shape
    if h % 2:
        return None

    midpoint = h // 2
    upper = grid[:midpoint]
    lower = grid[midpoint:]

    if np.any(upper) or not np.any(lower):
        return None

    return np.vstack((np.flipud(lower), lower))

def _spiral_seed(size: int, dtype):
    seed = np.full((size, size), 3, dtype=dtype)
    if size >= 3:
        seed[1, :-1] = 0
    if size >= 4:
        seed[1:-1, 1] = 0
        seed[1:-1, -2] = 0
        seed[-2, 1:-1] = 0
        seed[2, 1] = 3
    return seed

def rule_spiral(grid: np.ndarray):

    h, w = grid.shape
    if h != w or np.any(grid != 0):
        return None

    remainder = h % 4
    base_size = 4 if remainder == 0 else remainder
    block = _spiral_seed(base_size, grid.dtype)

    while block.shape[0] < h:
        n = block.shape[0] + 4
        grown = np.full((n, n), 3, dtype=grid.dtype)
        grown[2:-2, 2:-2] = block
        grown[1, :-1] = 0
        grown[1:-1, 1] = 0
        grown[1:-1, -2] = 0
        grown[-2, 1:-1] = 0
        grown[2, 1] = 3
        block = grown

    return block if block.shape == grid.shape else None

def rule_hollow(grid: np.ndarray):

    out = grid.copy()
    changed = False

    for color in map(int, np.unique(grid)):
        if color == 0:
            continue

        tagged = label(grid == color, connectivity=1)
        regions = regionprops(tagged)

        for region in regions:
            minr, minc, maxr, maxc = region.bbox
            height = maxr - minr
            width = maxc - minc

            if height < 2 or width < 2:
                continue

            patch = grid[minr:maxr, minc:maxc]
            mask = (patch == color)

            if not np.all(mask):
                continue

            hollow = np.zeros((height, width), dtype=grid.dtype)
            hollow[0, :] = color
            hollow[-1, :] = color
            hollow[:, 0] = color
            hollow[:, -1] = color

            out[minr:maxr, minc:maxc] = hollow
            changed = True

    return out if changed else None

def rule_blocks(grid: np.ndarray):

    vals = np.unique(grid)
    if 5 not in vals or np.any(~np.isin(vals, [0, 5])):
        return None

    seeded = grid == 5
    expanded = ndimage.binary_dilation(seeded, structure=three_ex_three)
    return expanded.astype(grid.dtype)

def rule_xpixel(grid: np.ndarray):

    pts = np.argwhere(grid != 0)
    if len(pts) != 1:
        return None

    r, c = map(int, pts[0])
    color = int(grid[r, c])

    h, w = grid.shape
    rows = np.arange(h)
    diag_a = c + (rows - r)
    diag_b = c - (rows - r)

    out = np.zeros_like(grid)

    keep_a = (0 <= diag_a) & (diag_a < w)
    keep_b = (0 <= diag_b) & (diag_b < w)

    out[rows[keep_a], diag_a[keep_a]] = color
    out[rows[keep_b], diag_b[keep_b]] = color

    return out

def rule_two(grid: np.ndarray):

    vals, counts = np.unique(grid[grid != 0], return_counts=True)
    if len(vals) != 2:
        return None

    pairs = sorted((int(cnt), int(val)) for val, cnt in zip(vals, counts))
    rare = pairs[0][1]

    out = grid.copy()
    out[out == rare] = 2
    return out

def rule_mask(grid: np.ndarray):

    vals = np.unique(grid[grid != 0])
    if len(vals) != 2 or 5 not in vals:
        return None

    fill = int(vals[0] if vals[1] == 5 else vals[1])
    out = np.zeros_like(grid)
    out[grid == 5] = fill
    return out

def rule_crop(grid: np.ndarray):

    return crop_it(grid)

def rule_swap(grid: np.ndarray):

    cropped = crop_it(grid)
    if cropped is None:
        return None

    vals = np.unique(cropped[cropped != 0])
    if len(vals) != 2:
        return None

    a, b = map(int, vals)
    lut = np.arange(max(10, int(cropped.max()) + 1), dtype=grid.dtype)
    lut[a], lut[b] = b, a
    return lut[cropped]

def rule_proj(grid: np.ndarray):

    height, width = grid.shape
    if height < 3 or width  < 3:
        return None

    top = int(grid[0, 1])
    bottom = int(grid[height - 1, 1])
    left = int(grid[1, 0])
    right = int(grid[1, width  - 1])

    if 0 in (top, bottom, left, right):
        return None

    if not np.all(grid[0, 1:-1] == top):
        return None
    if not np.all(grid[-1, 1:-1] == bottom):
        return None
    if not np.all(grid[1:-1, 0] == left):
        return None
    if not np.all(grid[1:-1, -1] == right):
        return None

    ogrid = np.zeros_like(grid)
    ogrid[0, :] = grid[0, :]
    ogrid[-1, :] = grid[-1, :]
    ogrid[:, 0] = grid[:, 0]
    ogrid[:, -1] = grid[:, -1]

    def project_target(value, r, c):
        if value == top:
            return 1, c
        if value == bottom:
            return height - 2, c
        if value == left:
            return r, 1
        if value == right:
            return r, width  - 2
        return None

    for row, col in np.argwhere(grid[1:-1, 1:-1] != 0):
        rr, cc = row + 1, col + 1
        value = int(grid[rr, cc])

        target = project_target(value, rr, cc)
        if target is None:
            continue

        tr, tc = target
        ogrid[tr, tc] = value

    return ogrid

rulesAB = [rule_mirror,
           rule_spiral,
           rule_hollow,
           rule_blocks,
           rule_xpixel,
           rule_two,
           rule_mask,
           lambda g: np.rot90(g, 1),
           lambda g: np.rot90(g, 2),
           rule_crop,
           rule_swap,
           rule_proj]
##################### Milestones AB #####################