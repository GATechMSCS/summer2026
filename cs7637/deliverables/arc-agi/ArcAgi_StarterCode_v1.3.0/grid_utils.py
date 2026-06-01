from skimage.measure import label, regionprops
from scipy import ndimage
import numpy as np

four_way = np.array([[0, 1, 0],
                     [1, 1, 1],
                     [0, 1, 0]],
                    dtype=np.uint8,)

def _find_separator_line(grid: np.ndarray):

    h, w = grid.shape

    for r in range(h):
        vals = np.unique(grid[r, :])
        if len(vals) == 1 and vals[0] != 0:
            top = grid[:r, :]
            bottom = grid[r + 1:, :]
            if top.size > 0 and top.shape == bottom.shape:
                return "h", r

    for c in range(w):
        vals = np.unique(grid[:, c])
        if len(vals) == 1 and vals[0] != 0:
            left = grid[:, :c]
            right = grid[:, c + 1:]
            if left.size > 0 and left.shape == right.shape:
                return "v", c

    return None

def split_on_separator(grid: np.ndarray):

    sep = _find_separator_line(grid)
    if sep is None:
        return None

    axis, idx = sep
    if axis == "h":
        return grid[:idx, :], grid[idx + 1:, :]
    return grid[:, :idx], grid[:, idx + 1:]

def _bbox_from_mask(mask: np.ndarray):

    props = regionprops(label(mask.astype(np.uint8), connectivity=1))
    if not props:
        return None

    pts = np.argwhere(mask)
    r0, c0 = pts.min(axis=0)
    r1, c1 = pts.max(axis=0)
    return int(r0), int(r1), int(c0), int(c1)

def find_all_components(grid: np.ndarray):

    found = []
    for color in map(int, np.unique(grid)):
        if color == 0:
            continue
        labeled, count = ndimage.label(grid == color, structure=four_way)
        for tag in range(1, count + 1):
            coords = np.argwhere(labeled == tag)
            found.append((color, [tuple(map(int, rc)) for rc in coords]))
    return found

def crop_nonzero_bbox(grid: np.ndarray):

    box = _bbox_from_mask(grid != 0)
    if box is None:
        return None

    r0, r1, c0, c1 = box
    return grid[r0:r1 + 1, c0:c1 + 1]

def detect_holes_and_border(grid: np.ndarray, shape_cells, bg_color, shape_color):

    h, w = grid.shape
    shape_mask = np.zeros((h, w), dtype=bool)
    for r, c in shape_cells:
        shape_mask[r, c] = True

    box = _bbox_from_mask(shape_mask)
    if box is None:
        return [], set()

    r0, r1, c0, c1 = box
    sub = shape_mask[r0:r1 + 1, c0:c1 + 1]
    non_shape = ~sub

    boundary = np.zeros_like(non_shape, dtype=bool)
    boundary[0, :] = non_shape[0, :]
    boundary[-1, :] = non_shape[-1, :]
    boundary[:, 0] = non_shape[:, 0]
    boundary[:, -1] = non_shape[:, -1]

    exterior = ndimage.binary_propagation(boundary, structure=four_way, mask=non_shape)
    holes_mask = non_shape & (~exterior)

    holes = []
    if np.any(holes_mask):
        hole_labels, hole_count = ndimage.label(holes_mask, structure=four_way)
        for tag in range(1, hole_count + 1):
            coords = np.argwhere(hole_labels == tag)
            holes.append([(int(r0 + rr), int(c0 + cc)) for rr, cc in coords])

    border_mask = (
        ndimage.binary_dilation(shape_mask, structure=four_way)
        & (~shape_mask)
        & (grid == bg_color)
    )
    border = set(tuple(map(int, rc)) for rc in np.argwhere(border_mask))
    return holes, border
