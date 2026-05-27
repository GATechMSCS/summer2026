import numpy as np

##################### Milestones C #####################
def quad_mirror(x):
        top = np.hstack([x, np.fliplr(x)])
        bottom = np.hstack([np.flipud(x), np.rot90(x, 2)])
        return np.vstack([top, bottom])

def move_three_one_step_toward_four(x):
    threes = np.argwhere(x == 3)
    fours = np.argwhere(x == 4)
    others = [int(c) for c in np.unique(x) if c not in (0, 3, 4)]
    if len(threes) != 1 or len(fours) != 1 or others:
        return None

    r3, c3 = map(int, threes[0])
    r4, c4 = map(int, fours[0])
    dr = 0 if r4 == r3 else (1 if r4 > r3 else -1)
    dc = 0 if c4 == c3 else (1 if c4 > c3 else -1)
    nr, nc = r3 + dr, c3 + dc
    if not (0 <= nr < x.shape[0] and 0 <= nc < x.shape[1]):
        return None

    out = x.copy()
    out[r3, c3] = 0
    out[nr, nc] = 3
    return out

def decorate_four_rectangle_corners_and_connect(x):
        pts = np.argwhere(x != 0)
        if len(pts) != 4:
            return None

        rows = sorted({int(r) for r, _ in pts})
        cols = sorted({int(c) for _, c in pts})
        if len(rows) != 2 or len(cols) != 2:
            return None

        r0, r1 = rows
        c0, c1 = cols
        corners = [(r0, c0), (r0, c1), (r1, c0), (r1, c1)]
        if any(x[r, c] == 0 for r, c in corners):
            return None

        colors = sorted({int(x[r, c]) for r, c in corners})
        if len(colors) != 2:
            return None

        a, b = colors
        if int(x[r0, c0]) != int(x[r1, c1]) or int(x[r0, c1]) != int(x[r1, c0]):
            return None
        if {int(x[r0, c0]), int(x[r0, c1])} != {a, b}:
            return None

        h, w = x.shape
        if r0 - 1 < 0 or r1 + 1 >= h or c0 - 1 < 0 or c1 + 1 >= w:
            return None

        out = np.zeros_like(x)
        for r, c in corners:
            center_color = int(x[r, c])
            surround_color = b if center_color == a else a
            out[r - 1:r + 2, c - 1:c + 2] = surround_color
            out[r, c] = center_color

        for c in range(c0 + 2, c1 - 1):
            if min(c - (c0 + 2), (c1 - 2) - c) % 2 == 0:
                out[r0, c] = 5
                out[r1, c] = 5

        for r in range(r0 + 2, r1 - 1):
            if min(r - (r0 + 2), (r1 - 2) - r) % 2 == 0:
                out[r, c0] = 5
                out[r, c1] = 5
        return out

def fold_across_five_separator_row(x):
    h, w = x.shape
    five_rows = [r for r in range(h) if np.all(x[r, :] == 5)]
    if len(five_rows) != 1:
        return None

    sep = five_rows[0]
    top = x[:sep, :]
    bottom = x[sep + 1:, :]
    if top.shape != bottom.shape or top.shape[0] == 0:
        return None

    out = top.copy()
    mask = bottom != 0
    out[mask] = bottom[mask]
    return out

def expand_leading_run_to_half_width_staircase(x):
    if x.shape[0] != 1 or x.shape[1] % 2 != 0:
        return None

    row = x[0]
    nz = np.flatnonzero(row != 0)
    if len(nz) == 0:
        return None

    run_len = len(nz)
    if not np.array_equal(nz, np.arange(run_len)):
        return None

    color = int(row[0])
    if np.any(row[:run_len] != color) or np.any(row[run_len:] != 0):
        return None

    h = x.shape[1] // 2
    out = np.zeros((h, x.shape[1]), dtype=x.dtype)
    for r in range(h):
        out[r, :run_len + r] = color
    return out

def neighbors4(self, r, c, h, w):
    if r > 0:
        yield r - 1, c
    if r + 1 < h:
        yield r + 1, c
    if c > 0:
        yield r, c - 1
    if c + 1 < w:
        yield r, c + 1

def fill_zero_regions_outer_three_inner_two(x):
    h, w = x.shape
    zero_seen = np.zeros((h, w), dtype=bool)
    out = x.copy()
    found_zero = False

    for r in range(h):
        for c in range(w):
            if x[r, c] != 0 or zero_seen[r, c]:
                continue
            found_zero = True
            stack = [(r, c)]
            zero_seen[r, c] = True
            comp = []
            touches_border = False
            while stack:
                rr, cc = stack.pop()
                comp.append((rr, cc))
                if rr in (0, h - 1) or cc in (0, w - 1):
                    touches_border = True
                for nr, nc in neighbors4(rr, cc, h, w):
                    if x[nr, nc] == 0 and not zero_seen[nr, nc]:
                        zero_seen[nr, nc] = True
                        stack.append((nr, nc))
            fill = 3 if touches_border else 2
            for rr, cc in comp:
                out[rr, cc] = fill

    return out if found_zero else None

def fill_rows_when_endpoints_match(x):
    h, w = x.shape
    if w < 2:
        return None
    out = x.copy()
    for r in range(h):
        left = int(x[r, 0])
        right = int(x[r, w - 1])
        if left != 0 and left == right and np.any(x[r, 1:w - 1] == 0):
            out[r, :] = left
    return out

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

def recolor_holey_one_components_to_eight(x):
    h, w = x.shape
    out = x.copy()
    changed = False
    values, counts = np.unique(x, return_counts=True)
    bg_color = int(values[np.argmax(counts)])

    foreground_colors = [int(c) for c in values if c != bg_color]
    if not foreground_colors:
        return None

    for color in foreground_colors:
        for comp in connected_components_of_color(x, color):
            comp_set = set(comp)
            rows = [r for r, _ in comp]
            cols = [c for _, c in comp]
            r0, r1 = min(rows), max(rows)
            c0, c1 = min(cols), max(cols)

            reachable = np.zeros((h, w), dtype=bool)
            stack = []
            for r in range(r0, r1 + 1):
                for c in range(c0, c1 + 1):
                    if r in (r0, r1) or c in (c0, c1):
                        if x[r, c] == bg_color and (r, c) not in comp_set and not reachable[r, c]:
                            reachable[r, c] = True
                            stack.append((r, c))

            while stack:
                r, c = stack.pop()
                for nr, nc in neighbors4(r, c, h, w):
                    if nr < r0 or nr > r1 or nc < c0 or nc > c1:
                        continue
                    if x[nr, nc] != bg_color or (nr, nc) in comp_set or reachable[nr, nc]:
                        continue
                    reachable[nr, nc] = True
                    stack.append((nr, nc))

            has_hole = False
            for r in range(r0, r1 + 1):
                for c in range(c0, c1 + 1):
                    if x[r, c] == bg_color and (r, c) not in comp_set and not reachable[r, c]:
                        has_hole = True
                        break
                if has_hole:
                    break

            if has_hole:
                for r, c in comp:
                    out[r, c] = 8
                    changed = True

    return out if changed else None

def overlay_three_equal_panels_left_to_right_priority(x):
    h, w = x.shape
    if h != 4 or w != 14:
        return None

    if not np.all(x[:, 4] == 2) or not np.all(x[:, 9] == 2):
        return None

    c1, c2 = 4, 9
    left = x[:, :c1]
    middle = x[:, c1 + 1:c2]
    right = x[:, c2 + 1:]
    if left.shape != middle.shape or middle.shape != right.shape:
        return None

    out = left.copy()
    mask = out == 0
    out[mask & (middle != 0)] = middle[mask & (middle != 0)]
    mask = out == 0
    out[mask & (right != 0)] = right[mask & (right != 0)]
    return out

def extend_single_marker_from_wedge_apex(x):
        colors = [int(c) for c in np.unique(x) if c != 0]
        if len(colors) != 2:
            return None

        counts = {c: int(np.sum(x == c)) for c in colors}
        marker_color = next((c for c in colors if counts[c] == 1), None)
        if marker_color is None:
            return None
        bulk_color = next(c for c in colors if c != marker_color)

        r, c = map(int, np.argwhere(x == marker_color)[0])
        bulk = np.argwhere(x == bulk_color)
        if bulk.size == 0:
            return None

        r0, c0 = bulk.min(axis=0)
        r1, c1 = bulk.max(axis=0)
        if r == r0:
            dr, dc = 1, 0
        elif r == r1:
            dr, dc = -1, 0
        elif c == c0:
            dr, dc = 0, 1
        elif c == c1:
            dr, dc = 0, -1
        else:
            return None

        out = x.copy()
        cr, cc = r, c
        # Skip over the wedge itself, then extend only through the empty region.
        while 0 <= cr < x.shape[0] and 0 <= cc < x.shape[1] and out[cr, cc] != 0:
            cr += dr
            cc += dc
        while 0 <= cr < x.shape[0] and 0 <= cc < x.shape[1]:
            out[cr, cc] = marker_color
            cr += dr
            cc += dc
        return out

def reflect_fives_outside_two_frame(x):
        colors = {int(c) for c in np.unique(x)}
        if not {2, 5}.issubset(colors) or any(c not in {0, 2, 5} for c in colors):
            return None

        twos = np.argwhere(x == 2)
        fives = np.argwhere(x == 5)
        if len(twos) == 0 or len(fives) == 0:
            return None

        out = x.copy()
        out[out == 5] = 0

        def longest_run(values):
            best = 0
            run = 0
            for value in values:
                run = run + 1 if value == 2 else 0
                best = max(best, run)
            return best

        row_runs = {r: longest_run(x[r, :]) for r in range(x.shape[0])}
        col_runs = {c: longest_run(x[:, c]) for c in range(x.shape[1])}
        best_h = max(row_runs.values(), default=0)
        best_v = max(col_runs.values(), default=0)

        if best_h <= 1 and best_v <= 1:
            return None

        if best_h > best_v:
            rows = [r for r, run in row_runs.items() if run == best_h]
            top_row, bottom_row = min(rows), max(rows)
            for r, c in fives:
                distances = [(abs(r - top_row), top_row), (abs(r - bottom_row), bottom_row)]
                best_dist = min(dist for dist, _ in distances)
                for dist, side_row in distances:
                    if dist != best_dist:
                        continue
                    rr = int(2 * side_row - r)
                    if not (0 <= rr < x.shape[0]):
                        return None
                    out[rr, c] = 5
        else:
            cols = [c for c, run in col_runs.items() if run == best_v]
            left_col, right_col = min(cols), max(cols)
            for r, c in fives:
                distances = [(abs(c - left_col), left_col), (abs(c - right_col), right_col)]
                best_dist = min(dist for dist, _ in distances)
                for dist, side_col in distances:
                    if dist != best_dist:
                        continue
                    cc = int(2 * side_col - c)
                    if not (0 <= cc < x.shape[1]):
                        return None
                    out[r, cc] = 5

        return out

def inner_shape_recolor_from_four_markers(x):
        nonzero_colors = [int(c) for c in np.unique(x) if c != 0]

        for marker_color in nonzero_colors:
            coords = np.argwhere(x == marker_color)
            if len(coords) != 4:
                continue

            rows = sorted(set(int(r) for r, _ in coords))
            cols = sorted(set(int(c) for _, c in coords))

            if len(rows) != 2 or len(cols) != 2:
                continue

            r0, r1 = rows
            c0, c1 = cols

            expected = {(r0, c0), (r0, c1), (r1, c0), (r1, c1)}
            actual = set((int(r), int(c)) for r, c in coords)
            if actual != expected:
                continue

            if r1 - r0 <= 1 or c1 - c0 <= 1:
                continue

            interior = x[r0 + 1:r1, c0 + 1:c1].copy()

            mask = (interior != 0) & (interior != marker_color)
            if not np.any(mask):
                continue

            interior[mask] = marker_color
            return interior

        return None

def extend_diag_from_1_and_2_blocks(x):
    out = x.copy()

    # color 1: top-left corner -> (-1, -1)
    coords1 = np.argwhere(x == 1)
    if len(coords1) == 4:
        rows1 = sorted(set(int(r) for r, _ in coords1))
        cols1 = sorted(set(int(c) for _, c in coords1))
        if len(rows1) == 2 and len(cols1) == 2:
            r0, r1 = rows1
            c0, c1 = cols1
            expected1 = {(r0, c0), (r0, c1), (r1, c0), (r1, c1)}
            actual1 = set((int(r), int(c)) for r, c in coords1)

            if actual1 == expected1:
                r, c = r0 - 1, c0 - 1
                while 0 <= r < x.shape[0] and 0 <= c < x.shape[1]:
                    out[r, c] = 1
                    r -= 1
                    c -= 1

    # color 2: bottom-right corner -> (+1, +1)
    coords2 = np.argwhere(x == 2)
    if len(coords2) == 4:
        rows2 = sorted(set(int(r) for r, _ in coords2))
        cols2 = sorted(set(int(c) for _, c in coords2))
        if len(rows2) == 2 and len(cols2) == 2:
            r0, r1 = rows2
            c0, c1 = cols2
            expected2 = {(r0, c0), (r0, c1), (r1, c0), (r1, c1)}
            actual2 = set((int(r), int(c)) for r, c in coords2)

            if actual2 == expected2:
                r, c = r1 + 1, c1 + 1
                while 0 <= r < x.shape[0] and 0 <= c < x.shape[1]:
                    out[r, c] = 2
                    r += 1
                    c += 1

    return out

def sort_colors_by_frequency_vertical(self, x):

        colors = [int(c) for c in np.unique(x) if c != 0]
        if not colors:
            return None

        counts = []
        for color in colors:
            cnt = int(np.sum(x == color))
            counts.append((color, cnt))

        # count desc, same count면 color asc
        counts.sort(key=lambda t: (-t[1], t[0]))

        max_count = counts[0][1]
        num_colors = len(counts)

        out = np.zeros((max_count, num_colors), dtype=x.dtype)

        for col_idx, (color, cnt) in enumerate(counts):
            out[:cnt, col_idx] = color

        return out
##################### Milestones C #####################

##################### Milestones C #####################
rulesC = [quad_mirror,
        lambda x: x.T,
        move_three_one_step_toward_four,
        decorate_four_rectangle_corners_and_connect,
        fold_across_five_separator_row,
        expand_leading_run_to_half_width_staircase,
        fill_zero_regions_outer_three_inner_two,
        fill_rows_when_endpoints_match,
        recolor_holey_one_components_to_eight,
        overlay_three_equal_panels_left_to_right_priority,
        extend_single_marker_from_wedge_apex,
        reflect_fives_outside_two_frame,
        inner_shape_recolor_from_four_markers,
        extend_diag_from_1_and_2_blocks,
        sort_colors_by_frequency_vertical]
##################### Milestones C #####################