import numpy as np

##################### Milestones AB #####################
def mirror_bottom_half_to_top(x):
    h, w = x.shape
    if h % 2 != 0:
        return None
    mid = h // 2
    top = x[:mid, :]
    bottom = x[mid:, :]
    if np.any(top != 0) or not np.any(bottom != 0):
        return None
    return np.vstack([np.flipud(bottom), bottom])

def draw_recursive_three_spiral_on_empty_square(x):
        h, w = x.shape
        if h != w or h < 1 or np.any(x != 0):
            return None

        base_patterns = {
            1: np.array([[3]], dtype=x.dtype),
            2: np.array([[3, 3], [3, 3]], dtype=x.dtype),
            3: np.array([[3, 3, 3], [0, 0, 3], [3, 3, 3]], dtype=x.dtype),
            4: np.array([[3, 3, 3, 3], [0, 0, 0, 3], [3, 3, 0, 3], [3, 3, 3, 3]], dtype=x.dtype),}

        def wrap(inner):
            n = inner.shape[0] + 4
            out = np.full((n, n), 3, dtype=x.dtype)
            out[2:n - 2, 2:n - 2] = inner
            out[1, :-1] = 0
            out[1:-1, 1] = 0
            out[1:-1, n - 2] = 0
            out[n - 2, 1:-1] = 0
            out[2, 1] = 3
            return out

        base_size = 4 if h % 4 == 0 else h % 4
        out = base_patterns[base_size]
        while out.shape[0] < h:
            out = wrap(out)
        return out if out.shape == x.shape else None

def neighbors4(r, c, h, w):
    if r > 0:
        yield r - 1, c
    if r + 1 < h:
        yield r + 1, c
    if c > 0:
        yield r, c - 1
    if c + 1 < w:
        yield r, c + 1

def connected_components_of_color(x, color):
    h, w = x.shape
    visited = np.zeros((h, w), dtype=bool)
    components = []

    for r in range(h):
        for c in range(w):
            if visited[r, c] or x[r, c] != color:
                continue

            stack = [(r, c)]
            visited[r, c] = True
            comp = []

            while stack:
                cr, cc = stack.pop()
                comp.append((cr, cc))
                for nr, nc in neighbors4(cr, cc, h, w):
                    if not visited[nr, nc] and x[nr, nc] == color:
                        visited[nr, nc] = True
                        stack.append((nr, nc))

            components.append(comp)

    return components

def hollow_solid_rectangles(x):
    out = x.copy()
    changed = False
    for color in [int(c) for c in np.unique(x) if c != 0]:
        comps = connected_components_of_color(x, color)
        for comp in comps:
            rows = [r for r, _ in comp]
            cols = [c for _, c in comp]
            r0, r1 = min(rows), max(rows)
            c0, c1 = min(cols), max(cols)
            if (r1 - r0 + 1) * (c1 - c0 + 1) != len(comp):
                return None
            if r1 - r0 < 1 or c1 - c0 < 1:
                continue
            out[r0:r1 + 1, c0:c1 + 1] = 0
            out[r0, c0:c1 + 1] = color
            out[r1, c0:c1 + 1] = color
            out[r0:r1 + 1, c0] = color
            out[r0:r1 + 1, c1] = color
            changed = True
    return out if changed else None

def five_markers_to_centered_three_by_three_blocks(x):
        colors = {int(c) for c in np.unique(x)}
        if any(c not in {0, 5} for c in colors) or 5 not in colors:
            return None

        out = np.zeros_like(x)
        for r, c in np.argwhere(x == 5):
            r0, r1 = max(0, r - 1), min(x.shape[0], r + 2)
            c0, c1 = max(0, c - 1), min(x.shape[1], c + 2)
            out[r0:r1, c0:c1] = 1
        return out

def draw_x_through_single_colored_seed(x):
    pts = np.argwhere(x != 0)
    if len(pts) != 1:
        return None
    r, c = map(int, pts[0])
    color = int(x[r, c])
    out = np.zeros_like(x)
    h, w = x.shape
    for rr in range(h):
        cc = c + (rr - r)
        if 0 <= cc < w:
            out[rr, cc] = color
        cc = c - (rr - r)
        if 0 <= cc < w:
            out[rr, cc] = color
    return out

def replace_least_frequent_nonzero_color_with_two(x):
    colors = sorted(int(c) for c in np.unique(x) if c != 0)
    if len(colors) != 2:
        return None

    counts = {color: int(np.sum(x == color)) for color in colors}
    src_color = min(colors, key=lambda color: (counts[color], color))
    out = x.copy()
    out[out == src_color] = 2
    return out

def keep_five_mask_recolored_to_other(x):
    colors = [int(c) for c in np.unique(x) if c != 0]
    if len(colors) != 2 or 5 not in colors:
        return None
    keep_color = next(c for c in colors if c != 5)
    out = np.zeros_like(x)
    out[x == 5] = keep_color
    return out

def tight_crop(x):
    coords = np.argwhere(x != 0)
    if coords.size == 0:
        return None
    r0, c0 = coords.min(axis=0)
    r1, c1 = coords.max(axis=0)
    return x[r0:r1 + 1, c0:c1 + 1]

def crop_nonzero(x):
    return tight_crop(x)

def crop_and_swap_two_colors(x):
    cropped = crop_nonzero(x)
    if cropped is None:
        return None

    colors = np.unique(cropped)
    colors = colors[colors != 0]
    if len(colors) != 2:
        return None

    a, b = colors
    out = cropped.copy()
    out[cropped == a] = b
    out[cropped == b] = a
    return out
##################### Milestones AB #####################

##################### Milestones AB #####################
rulesAB = [mirror_bottom_half_to_top,
        draw_recursive_three_spiral_on_empty_square,
        hollow_solid_rectangles,
        five_markers_to_centered_three_by_three_blocks,
        draw_x_through_single_colored_seed,
        replace_least_frequent_nonzero_color_with_two,
        keep_five_mask_recolored_to_other,
        lambda x: np.rot90(x, 1),
        lambda x: np.rot90(x, 2),
        crop_nonzero,
        crop_and_swap_two_colors,]
##################### Milestones AB #####################