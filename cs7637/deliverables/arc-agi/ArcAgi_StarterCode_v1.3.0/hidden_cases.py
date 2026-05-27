import numpy as np

##################### Hidden Cases #####################
def pair_to_line_same_row(x):
        out = np.zeros_like(x)
        colors = [int(c) for c in np.unique(x) if c != 0]

        changed = False
        for color in colors:
            coords = np.argwhere(x == color)

            if len(coords) == 1:
                r, c = coords[0]
                out[r, c] = color
                changed = True

            elif len(coords) == 2:
                (r1, c1), (r2, c2) = coords
                if r1 == r2:
                    cmin, cmax = min(c1, c2), max(c1, c2)
                    out[r1, cmin:cmax + 1] = color
                    changed = True
                elif c1 == c2:
                    return None
                else:
                    return None
            else:
                return None

        return out if changed else None

def pair_to_line_same_col(x):
    out = np.zeros_like(x)
    colors = [int(c) for c in np.unique(x) if c != 0]

    changed = False
    for color in colors:
        coords = np.argwhere(x == color)

        if len(coords) == 1:
            r, c = coords[0]
            out[r, c] = color
            changed = True

        elif len(coords) == 2:
            (r1, c1), (r2, c2) = coords
            if c1 == c2:
                rmin, rmax = min(r1, r2), max(r1, r2)
                out[rmin:rmax + 1, c1] = color
                changed = True
            elif r1 == r2:
                return None
            else:
                return None
        else:
            return None

    return out if changed else None

def draw_line_between_twos_with_one_to_three(self, x):
    coords = [tuple(int(v) for v in rc) for rc in np.argwhere(x == 2)]
    if len(coords) != 2:
        return None

    (r1, c1), (r2, c2) = coords
    dr = r2 - r1
    dc = c2 - c1
    steps = max(abs(dr), abs(dc))
    if steps == 0:
        return None

    points = []
    prev = None
    for k in range(steps + 1):
        r = int(round(r1 + dr * k / steps))
        c = int(round(c1 + dc * k / steps))
        point = (r, c)
        if point != prev:
            points.append(point)
            prev = point

    out = x.copy()
    for r, c in points:
        out[r, c] = 3 if x[r, c] == 1 else 2

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

def draw_three_spiral_on_empty_rectangle(x):
        h, w = x.shape
        if h < 2 or w < 2 or np.any(x != 0):
            return None

        out = np.full_like(x, 3)

        def can_step(nr, nc, cr, cc):
            if not (0 <= nr < h and 0 <= nc < w):
                return False
            if out[nr, nc] == 0:
                return False
            if nr in (0, h - 1) or nc in (0, w - 1):
                return False
            for ar, ac in neighbors4(nr, nc, h, w):
                if (ar, ac) != (cr, cc) and out[ar, ac] == 0:
                    return False
            return True

        r, c = 1, 0
        out[r, c] = 0
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        dir_idx = 0
        while True:
            dr, dc = directions[dir_idx]
            nr, nc = r + dr, c + dc
            if can_step(nr, nc, r, c):
                r, c = nr, nc
                out[r, c] = 0
                continue
            dir_idx = (dir_idx + 1) % 4
            dr, dc = directions[dir_idx]
            nr, nc = r + dr, c + dc
            if can_step(nr, nc, r, c):
                r, c = nr, nc
                out[r, c] = 0
                continue
            break

        return out

def project_border_color_hits_to_inner_edges(x):
        h, w = x.shape
        if h < 3 or w < 3:
            return None

        top_color = int(x[0, 1])
        bottom_color = int(x[h - 1, 1])
        left_color = int(x[1, 0])
        right_color = int(x[1, w - 1])
        if 0 in (top_color, bottom_color, left_color, right_color):
            return None
        if not np.all(x[0, 1:w - 1] == top_color):
            return None
        if not np.all(x[h - 1, 1:w - 1] == bottom_color):
            return None
        if not np.all(x[1:h - 1, 0] == left_color):
            return None
        if not np.all(x[1:h - 1, w - 1] == right_color):
            return None

        out = np.zeros_like(x)
        out[0, :] = x[0, :]
        out[h - 1, :] = x[h - 1, :]
        out[:, 0] = x[:, 0]
        out[:, w - 1] = x[:, w - 1]

        for r in range(1, h - 1):
            for c in range(1, w - 1):
                color = int(x[r, c])
                candidates = []
                if color == top_color:
                    candidates.append((r - 1, 1, c))
                if color == bottom_color:
                    candidates.append((h - 2 - r, h - 2, c))
                if color == left_color:
                    candidates.append((c - 1, r, 1))
                if color == right_color:
                    candidates.append((w - 2 - c, r, w - 2))

                if not candidates:
                    continue

                best_dist = min(dist for dist, _, _ in candidates)
                for dist, rr, cc in candidates:
                    if dist == best_dist:
                        out[rr, cc] = color

        return out

def find_flower_centers(x, color=2):
        h, w = x.shape
        centers = []
        for r in range(1, h - 1):
            for c in range(1, w - 1):
                if x[r, c] != 0:
                    continue
                if x[r - 1, c] != color or x[r + 1, c] != color:
                    continue
                if x[r, c - 1] != color or x[r, c + 1] != color:
                    continue
                centers.append((r, c))
        return centers

def connect_flower_centers_with_line_color(x, line_color):
        candidate_colors = [int(c) for c in np.unique(x) if c != 0]
        centers = []
        for color in candidate_colors:
            centers = find_flower_centers(x, color=color)
            if len(centers) >= 2:
                break
        if len(centers) < 2:
            return None

        out = x.copy()
        changed = False

        rows = {}
        cols = {}
        for r, c in centers:
            rows.setdefault(r, []).append(c)
            cols.setdefault(c, []).append(r)

        for r, cols_in_row in rows.items():
            cols_in_row.sort()
            for left, right in zip(cols_in_row, cols_in_row[1:]):
                for c in range(left + 1, right):
                    if out[r, c] == 0:
                        out[r, c] = line_color
                        changed = True

        for c, rows_in_col in cols.items():
            rows_in_col.sort()
            for top, bottom in zip(rows_in_col, rows_in_col[1:]):
                for r in range(top + 1, bottom):
                    if out[r, c] == 0:
                        out[r, c] = line_color
                        changed = True

        return out if changed else None

def connect_flower_centers_with_ones(x):
        return connect_flower_centers_with_line_color(x, line_color=1)

def project_border_color_hits_to_all_matching_edges(x):
        h, w = x.shape
        if h < 3 or w < 3:
            return None

        top_color = int(x[0, 1])
        bottom_color = int(x[h - 1, 1])
        left_color = int(x[1, 0])
        right_color = int(x[1, w - 1])
        if 0 in (top_color, bottom_color, left_color, right_color):
            return None
        if not np.all(x[0, 1:w - 1] == top_color):
            return None
        if not np.all(x[h - 1, 1:w - 1] == bottom_color):
            return None
        if not np.all(x[1:h - 1, 0] == left_color):
            return None
        if not np.all(x[1:h - 1, w - 1] == right_color):
            return None

        out = np.zeros_like(x)
        out[0, :] = x[0, :]
        out[h - 1, :] = x[h - 1, :]
        out[:, 0] = x[:, 0]
        out[:, w - 1] = x[:, w - 1]

        for r in range(1, h - 1):
            for c in range(1, w - 1):
                color = int(x[r, c])
                if color == top_color:
                    out[1, c] = color
                if color == bottom_color:
                    out[h - 2, c] = color
                if color == left_color:
                    out[r, 1] = color
                if color == right_color:
                    out[r, w - 2] = color

        return out

def mirror_propagate_across_full_separators(x):
        h, w = x.shape
        colors = [int(c) for c in np.unique(x) if c != 0]
        if not colors:
            return None

        sep_color = max(colors, key=lambda c: int(np.sum(x == c)))
        sep_rows = [r for r in range(h) if np.all(x[r, :] == sep_color)]
        sep_cols = [c for c in range(w) if np.all(x[:, c] == sep_color)]
        if not sep_rows and not sep_cols:
            return None

        out = x.copy()
        changed = False

        row_edges = [-1] + sep_rows + [h]
        row_spans = [(row_edges[i] + 1, row_edges[i + 1]) for i in range(len(row_edges) - 1)]

        col_edges = [-1] + sep_cols + [w]
        col_spans = [(col_edges[i] + 1, col_edges[i + 1]) for i in range(len(col_edges) - 1)]

        for sep_idx, sc in enumerate(sep_cols, start=1):
            left_c0, left_c1 = col_spans[sep_idx - 1]
            right_c0, right_c1 = col_spans[sep_idx]
            left_w = left_c1 - left_c0
            right_w = right_c1 - right_c0
            if left_w != right_w or left_w <= 0:
                continue

            reference_pairs = []
            for r0, r1 in row_spans:
                if r1 <= r0:
                    continue
                left_block = x[r0:r1, left_c0:left_c1]
                right_block = x[r0:r1, right_c0:right_c1]
                if np.any(left_block != 0) and np.any(right_block != 0) and np.array_equal(np.fliplr(left_block), right_block):
                    reference_pairs.append(left_block.copy())

            if not reference_pairs:
                continue

            for r0, r1 in row_spans:
                if r1 <= r0:
                    continue
                left_block = x[r0:r1, left_c0:left_c1]
                right_block = x[r0:r1, right_c0:right_c1]

                left_nonzero = np.any(left_block != 0)
                right_nonzero = np.any(right_block != 0)

                if left_nonzero and not right_nonzero:
                    if any(np.array_equal(left_block, ref) for ref in reference_pairs):
                        out[r0:r1, right_c0:right_c1] = np.fliplr(left_block)
                        changed = True
                elif right_nonzero and not left_nonzero:
                    if any(np.array_equal(np.fliplr(right_block), ref) for ref in reference_pairs):
                        out[r0:r1, left_c0:left_c1] = np.fliplr(right_block)
                        changed = True

        return out if changed else None

def replace_six_with_two_keep_seven(x):
    colors = sorted(int(c) for c in np.unique(x) if c != 0)
    if colors != [6, 7]:
        return None

    out = x.copy()
    out[out == 6] = 2
    return out

def replace_min_nonzero_color_with_two(x):
        colors = sorted(int(c) for c in np.unique(x) if c != 0)
        if len(colors) != 2:
            return None

        out = x.copy()
        out[out == colors[0]] = 2
        return out
##################### Hidden Cases #####################

##################### Hidden Cases #####################
rulesH = [lambda x: np.rot90(x, 3),
            lambda x: np.flipud(x),
            lambda x: np.fliplr(x),
            lambda x: x.copy(),
            pair_to_line_same_row,
            pair_to_line_same_col,
            draw_line_between_twos_with_one_to_three,
            draw_three_spiral_on_empty_rectangle,
            project_border_color_hits_to_inner_edges,
            connect_flower_centers_with_ones,
            project_border_color_hits_to_all_matching_edges,
            mirror_propagate_across_full_separators,
            replace_six_with_two_keep_seven,
            replace_min_nonzero_color_with_two]
##################### Hidden Cases #####################