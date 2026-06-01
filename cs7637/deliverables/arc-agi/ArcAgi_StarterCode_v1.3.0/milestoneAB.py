from skimage.measure import label, regionprops
from grid_utils import crop_nonzero_bbox
from scipy import ndimage
import numpy as np

##################### Milestones AB #####################
four_way = np.array([[0, 1, 0],
                     [1, 1, 1],
                     [0, 1, 0]],
                    dtype=np.uint8,)
three_ex_three = np.ones((3, 3), dtype=bool)

def rule_mirror_bottom_to_top(grid: np.ndarray):
    h, _ = grid.shape
    if h % 2:
        return None

    mid = h // 2
    upper = grid[:mid]
    lower = grid[mid:]

    if np.any(upper) or not np.any(lower):
        return None

    return np.vstack((np.flipud(lower), lower))

def rule_recursive_three_spiral(grid: np.ndarray):

    h, w = grid.shape
    if h != w or np.any(grid != 0):
        return None

    seeds = {1: np.array([[3]], dtype=grid.dtype),
             2: np.array([[3, 3], [3, 3]], dtype=grid.dtype),
             3: np.array([[3, 3, 3],
                          [0, 0, 3],
                          [3, 3, 3]], dtype=grid.dtype),
             4: np.array([[3, 3, 3, 3],
                          [0, 0, 0, 3],
                          [3, 3, 0, 3],
                          [3, 3, 3, 3]], dtype=grid.dtype),}

    block = seeds[4 if h % 4 == 0 else h % 4]

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

def rule_hollow_rectangles(grid: np.ndarray):

    out = grid.copy()
    changed = False

    for color in map(int, np.unique(grid)):
        if color == 0:
            continue

        tagged = label(grid == color, connectivity=1)

        for region in regionprops(tagged):
            minr, minc, maxr, maxc = region.bbox
            height = maxr - minr
            width = maxc - minc

            if height == 1 or width == 1:
                continue

            if region.area != height * width:
                return None

            patch = grid[minr:maxr, minc:maxc]
            if not np.all(patch == color):
                return None

            out[minr:maxr, minc:maxc] = 0
            out[minr, minc:maxc] = color
            out[maxr - 1, minc:maxc] = color
            out[minr:maxr, minc] = color
            out[minr:maxr, maxc - 1] = color
            changed = True

    return out if changed else None

def rule_five_to_centered_blocks(grid: np.ndarray):

    vals = np.unique(grid)
    if 5 not in vals or np.any(~np.isin(vals, [0, 5])):
        return None

    seeded = grid == 5
    expanded = ndimage.binary_dilation(seeded, structure=three_ex_three)
    return expanded.astype(grid.dtype)

def rule_x_through_single_pixel(grid: np.ndarray):

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

def rule_rare_color_to_two(grid: np.ndarray):

    vals, counts = np.unique(grid[grid != 0], return_counts=True)
    if len(vals) != 2:
        return None

    pairs = sorted((int(cnt), int(val)) for val, cnt in zip(vals, counts))
    rare = pairs[0][1]

    out = grid.copy()
    out[out == rare] = 2
    return out

def rule_keep_five_mask_other_color(grid: np.ndarray):

    vals = np.unique(grid[grid != 0])
    if len(vals) != 2 or 5 not in vals:
        return None

    fill = int(vals[0] if vals[1] == 5 else vals[1])
    out = np.zeros_like(grid)
    out[grid == 5] = fill
    return out

def rule_crop_nonzero(grid: np.ndarray):

    return crop_nonzero_bbox(grid)

def rule_crop_and_swap_two(grid: np.ndarray):

    cropped = crop_nonzero_bbox(grid)
    if cropped is None:
        return None

    vals = np.unique(cropped[cropped != 0])
    if len(vals) != 2:
        return None

    a, b = map(int, vals)
    lut = np.arange(max(10, int(cropped.max()) + 1), dtype=grid.dtype)
    lut[a], lut[b] = b, a
    return lut[cropped]

def border_projection_vertical_first(grid: np.ndarray):

    h, w = grid.shape
    if h < 3 or w < 3:
        return None

    top = int(grid[0, 1])
    bottom = int(grid[h - 1, 1])
    left = int(grid[1, 0])
    right = int(grid[1, w - 1])

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

    out = np.zeros_like(grid)
    out[0, :] = grid[0, :]
    out[-1, :] = grid[-1, :]
    out[:, 0] = grid[:, 0]
    out[:, -1] = grid[:, -1]

    edge_targets = {
        top: lambda r, c: ("v", r - 1, 1, c),
        bottom: lambda r, c: ("v", h - 2 - r, h - 2, c),
        left: lambda r, c: ("h", c - 1, r, 1),
        right: lambda r, c: ("h", w - 2 - c, r, w - 2),}

    for r, c in np.argwhere(grid[1:-1, 1:-1] != 0):
        rr, cc = r + 1, c + 1
        value = int(grid[rr, cc])

        if value not in edge_targets:
            continue

        axis, dist, tr, tc = edge_targets[value](rr, cc)
        candidates = [(dist, tr, tc)]

        if axis == "v":
            best = min(d for d, _, _ in candidates)
        else:
            best = min(d for d, _, _ in candidates)

        for d, tr, tc in candidates:
            if d == best:
                out[tr, tc] = value

    return out

rulesAB = [rule_mirror_bottom_to_top,
           rule_recursive_three_spiral,
           rule_hollow_rectangles,
           rule_five_to_centered_blocks,
           rule_x_through_single_pixel,
           rule_rare_color_to_two,
           rule_keep_five_mask_other_color,
           lambda g: np.rot90(g, 1),
           lambda g: np.rot90(g, 2),
           rule_crop_nonzero,
           rule_crop_and_swap_two,
           border_projection_vertical_first,]
##################### Milestones AB #####################