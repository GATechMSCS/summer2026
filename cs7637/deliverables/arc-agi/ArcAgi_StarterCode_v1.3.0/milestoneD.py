import numpy as np

#################### Milestones D #####################
def xor_top_bottom_masks_to_six(x):
    h, w = x.shape
    if h != 6:
        return None

    top = x[:3, :]
    bottom = x[3:, :]
    top_mask = top != 0
    bottom_mask = bottom != 0
    xor_mask = np.logical_xor(top_mask, bottom_mask)

    out = np.zeros((3, w), dtype=x.dtype)
    out[xor_mask] = 6
    return out

def expand_single_two_to_v_with_inner_diagonals(x):
    return expand_single_two_to_v_with_inner_diagonals_variant(x, row_offset=3, base_shift=1)

def expand_single_two_to_v_with_inner_diagonals_variant(x, row_offset=3, base_shift=1):
    transposed = False
    if x.ndim != 2:
        return None
    if x.shape[0] == 1:
        row = x
    elif x.shape[1] == 1:
        row = x.T
        transposed = True
    else:
        return None

    coords = np.argwhere(row == 2)
    nonzero = np.argwhere(row != 0)
    if len(coords) != 1 or len(nonzero) != 1:
        return None

    _, pivot = coords[0]
    n = row.shape[1]
    out = np.zeros((n, n), dtype=row.dtype)

    for r in range(n):
        left = pivot - r
        right = pivot + r
        if 0 <= left < n:
            out[r, left] = 2
        if 0 <= right < n:
            out[r, right] = 2

    m = 0
    while True:
        base_c = pivot - base_shift - 2 * m
        start_c = max(0, base_c)
        start_r = row_offset + 2 * m + max(0, -base_c)

        if start_r >= n:
            break

        r, c = start_r, start_c
        while r < n and c < n:
            out[r, c] = 1
            r += 1
            c += 1

        m += 1

    return out.T if transposed else out

def marker_frame_to_small_staircase(x):
    marker_colors = [int(c) for c in np.unique(x) if c not in (0, 1)]
    if len(marker_colors) != 1:
        return None

    ones = np.argwhere(x == 1)
    if len(ones) == 0:
        return None

    r0, r1 = int(ones[:, 0].min()), int(ones[:, 0].max())
    c0, c1 = int(ones[:, 1].min()), int(ones[:, 1].max())
    color = marker_colors[0]
    inside_count = int(np.sum(x[r0:r1 + 1, c0:c1 + 1] == color))
    out = np.zeros((3, 3), dtype=x.dtype)
    for idx in range(min(inside_count, 9)):
        out[idx // 3, idx % 3] = color
    return out

def complete_missing_panel_by_separator_mirroring(x):
    h, w = x.shape
    colors = [int(c) for c in np.unique(x) if c != 0]
    if not colors:
        return None

    sep_color = max(colors, key=lambda c: int(np.sum(x == c)))
    sep_rows = [r for r in range(h) if np.all(x[r, :] == sep_color)]
    sep_cols = [c for c in range(w) if np.all(x[:, c] == sep_color)]
    if not sep_rows or not sep_cols:
        return None

    row_edges = [-1] + sep_rows + [h]
    col_edges = [-1] + sep_cols + [w]
    row_spans = [(row_edges[i] + 1, row_edges[i + 1]) for i in range(len(row_edges) - 1)]
    col_spans = [(col_edges[i] + 1, col_edges[i + 1]) for i in range(len(col_edges) - 1)]

    out = x.copy()
    changed = False

    def get_block(grid, ri, ci):
        r0, r1 = row_spans[ri]
        c0, c1 = col_spans[ci]
        if r0 >= r1 or c0 >= c1:
            return None
        return grid[r0:r1, c0:c1]

    def set_block(grid, ri, ci, block):
        r0, r1 = row_spans[ri]
        c0, c1 = col_spans[ci]
        grid[r0:r1, c0:c1] = block

    def nonzero(block):
        return block is not None and np.any(block != 0)

    progress = True
    while progress:
        progress = False
        for ri in range(len(row_spans) - 1):
            for ci in range(len(col_spans) - 1):
                tl = get_block(out, ri, ci)
                tr = get_block(out, ri, ci + 1)
                bl = get_block(out, ri + 1, ci)
                br = get_block(out, ri + 1, ci + 1)
                blocks = [tl, tr, bl, br]
                present = [nonzero(b) for b in blocks]
                if sum(present) != 3:
                    continue

                missing = present.index(False)
                candidates = []

                if missing == 0:
                    if nonzero(tr):
                        candidates.append(np.fliplr(tr))
                    if nonzero(bl):
                        candidates.append(np.flipud(bl))
                    if nonzero(br):
                        candidates.append(np.flipud(np.fliplr(br)))
                elif missing == 1:
                    if nonzero(tl):
                        candidates.append(np.fliplr(tl))
                    if nonzero(br):
                        candidates.append(np.flipud(br))
                    if nonzero(bl):
                        candidates.append(np.flipud(np.fliplr(bl)))
                elif missing == 2:
                    if nonzero(tl):
                        candidates.append(np.flipud(tl))
                    if nonzero(br):
                        candidates.append(np.fliplr(br))
                    if nonzero(tr):
                        candidates.append(np.flipud(np.fliplr(tr)))
                else:
                    if nonzero(tr):
                        candidates.append(np.flipud(tr))
                    if nonzero(bl):
                        candidates.append(np.fliplr(bl))
                    if nonzero(tl):
                        candidates.append(np.flipud(np.fliplr(tl)))

                if not candidates:
                    continue

                target = candidates[0]
                if any(c.shape != target.shape or not np.array_equal(c, target) for c in candidates[1:]):
                    continue

                if missing == 0:
                    set_block(out, ri, ci, target)
                elif missing == 1:
                    set_block(out, ri, ci + 1, target)
                elif missing == 2:
                    set_block(out, ri + 1, ci, target)
                else:
                    set_block(out, ri + 1, ci + 1, target)
                changed = True
                progress = True

    return out if changed else None

def trace_threes_between_single_one_and_two(x):
    return trace_two_point_path(x, force_initial_diagonal=True, start_mode="two")

def trace_two_point_path(x, force_initial_diagonal=True, start_mode="two"):
    ones = np.argwhere(x == 1)
    twos = np.argwhere(x == 2)
    others = [int(c) for c in np.unique(x) if c not in (0, 1, 2)]
    if len(ones) != 1 or len(twos) != 1 or others:
        return None

    one = tuple(int(v) for v in ones[0])
    two = tuple(int(v) for v in twos[0])
    if start_mode == "upper":
        start, end = sorted([one, two], key=lambda rc: (rc[0], rc[1]))
    elif start_mode == "one":
        start, end = one, two
    else:
        start, end = two, one

    rs, cs = start
    re, ce = end
    dr = 1 if re > rs else -1 if re < rs else 0
    dc = 1 if ce > cs else -1 if ce < cs else 0
    if dr == 0 and dc == 0:
        return None

    out = x.copy()
    cr, cc = rs, cs

    if force_initial_diagonal and dr != 0 and dc != 0:
        cr += dr
        cc += dc
        if (cr, cc) != (re, ce):
            out[cr, cc] = 3

    while True:
        rem_r = re - cr
        rem_c = ce - cc
        if max(abs(rem_r), abs(rem_c)) <= 1:
            break

        if abs(rem_r) == abs(rem_c):
            cr += 1 if rem_r > 0 else -1
            cc += 1 if rem_c > 0 else -1
        elif abs(rem_r) > abs(rem_c):
            cr += 1 if rem_r > 0 else -1
        else:
            cc += 1 if rem_c > 0 else -1

        if (cr, cc) == (re, ce):
            break
        out[cr, cc] = 3

    return out

def surround_holey_ones_with_twos_and_fill_inner_edge_with_threes(x):
        return surround_holey_ones_with_variant(x, fill_all_holes=False, hole_neighbor_mode=8)

def neighbors4(self, r, c, h, w):
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

def surround_holey_ones_with_variant(x, fill_all_holes=False, hole_neighbor_mode=8):
    h, w = x.shape
    out = x.copy()
    changed = False

    comps = connected_components_of_color(x, 1)
    if not comps:
        return None

    for comp in comps:
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
                    if (r, c) not in comp_set and x[r, c] == 0 and not reachable[r, c]:
                        reachable[r, c] = True
                        stack.append((r, c))

        while stack:
            r, c = stack.pop()
            for nr, nc in neighbors4(r, c, h, w):
                if nr < r0 or nr > r1 or nc < c0 or nc > c1:
                    continue
                if (nr, nc) in comp_set or x[nr, nc] != 0 or reachable[nr, nc]:
                    continue
                reachable[nr, nc] = True
                stack.append((nr, nc))

        holes = []
        for r in range(r0, r1 + 1):
            for c in range(c0, c1 + 1):
                if x[r, c] == 0 and not reachable[r, c] and (r, c) not in comp_set:
                    holes.append((r, c))

        if not holes:
            continue

        # 8-neighbor outer ring.
        for r, c in comp:
            for nr in range(r - 1, r + 2):
                for nc in range(c - 1, c + 2):
                    if 0 <= nr < h and 0 <= nc < w and (nr, nc) not in comp_set and x[nr, nc] == 0:
                        if out[nr, nc] == 0:
                            out[nr, nc] = 2
                            changed = True

        for r, c in holes:
            near_component = False
            if hole_neighbor_mode == 4:
                for nr, nc in neighbors4(r, c, h, w):
                    if (nr, nc) in comp_set:
                        near_component = True
                        break
            else:
                for nr in range(r - 1, r + 2):
                    for nc in range(c - 1, c + 2):
                        if (nr, nc) == (r, c):
                            continue
                        if 0 <= nr < h and 0 <= nc < w and (nr, nc) in comp_set:
                            near_component = True
                            break
                    if near_component:
                        break

            if fill_all_holes or near_component:
                out[r, c] = 3
                changed = True
            elif out[r, c] == 2:
                out[r, c] = 0

    return out

def all_nonzero_components(x):
    components = []
    for color in [int(c) for c in np.unique(x) if c != 0]:
        for comp in connected_components_of_color(x, color):
            components.append((color, comp))
    return components

def fill_closed_barrier_with_majority_color(x):
        out = np.zeros_like(x)
        changed = False
        h, w = x.shape

        barrier_components = []
        for color, comp in all_nonzero_components(x):
            if len(comp) < 5:
                continue

            comp_set = set(comp)
            barrier_components.append((color, comp_set))
            for r, c in comp:
                out[r, c] = color
                if x[r, c] != color:
                    changed = True

        if not barrier_components:
            return None

        for barrier_color, comp_set in barrier_components:
            reachable = np.zeros((h, w), dtype=bool)
            stack = []

            for r in range(h):
                for c in [0, w - 1]:
                    if (r, c) not in comp_set and not reachable[r, c]:
                        reachable[r, c] = True
                        stack.append((r, c))
            for c in range(w):
                for r in [0, h - 1]:
                    if (r, c) not in comp_set and not reachable[r, c]:
                        reachable[r, c] = True
                        stack.append((r, c))

            while stack:
                r, c = stack.pop()
                for nr, nc in neighbors4(r, c, h, w):
                    if (nr, nc) in comp_set or reachable[nr, nc]:
                        continue
                    reachable[nr, nc] = True
                    stack.append((nr, nc))

            visited = np.zeros((h, w), dtype=bool)
            for r in range(h):
                for c in range(w):
                    if (r, c) in comp_set or reachable[r, c] or visited[r, c]:
                        continue

                    region = []
                    region_stack = [(r, c)]
                    visited[r, c] = True

                    while region_stack:
                        cr, cc = region_stack.pop()
                        region.append((cr, cc))
                        for nr, nc in neighbors4(cr, cc, h, w):
                            if (nr, nc) in comp_set or reachable[nr, nc] or visited[nr, nc]:
                                continue
                            visited[nr, nc] = True
                            region_stack.append((nr, nc))

                    region_colors = [
                        int(x[rr, cc]) for rr, cc in region
                        if x[rr, cc] != 0 and (rr, cc) not in comp_set
                    ]
                    if not region_colors:
                        continue

                    counts = {}
                    for color in region_colors:
                        counts[color] = counts.get(color, 0) + 1
                    max_count = max(counts.values())
                    fill_color = min(color for color, cnt in counts.items() if cnt == max_count)

                    for rr, cc in region:
                        if out[rr, cc] != fill_color:
                            out[rr, cc] = fill_color
                            if x[rr, cc] != fill_color:
                                changed = True

        return out if changed else None

def count_panel_blocks_to_staircase(x):
    colors = [int(c) for c in np.unique(x) if c != 0]
    if not colors:
        return None

    # The dominant separator color forms full rows/cols.
    sep_color = max(colors, key=lambda color: int(np.sum(x == color)))
    counts = {}

    h, w = x.shape
    for r in range(h - 1):
        for c in range(w - 1):
            block = x[r:r + 2, c:c + 2]
            vals = np.unique(block)
            if len(vals) != 1:
                continue
            color = int(vals[0])
            if color == 0 or color == sep_color:
                continue
            counts.setdefault(color, set()).add((r, c))

    if not counts:
        return None

    items = sorted(((color, len(pos)) for color, pos in counts.items()), key=lambda t: (t[1], t[0]))
    out = np.zeros((len(items), max(cnt for _, cnt in items)), dtype=x.dtype)
    for r, (color, cnt) in enumerate(items):
        out[r, :cnt] = color
    return out

def largest_nonzero_component_bbox(x):
    h, w = x.shape
    visited = np.zeros((h, w), dtype=bool)
    best = None

    for r in range(h):
        for c in range(w):
            if visited[r, c] or x[r, c] == 0:
                continue

            stack = [(r, c)]
            visited[r, c] = True
            comp = []

            while stack:
                cr, cc = stack.pop()
                comp.append((cr, cc))
                for nr, nc in neighbors4(cr, cc, h, w):
                    if not visited[nr, nc] and x[nr, nc] != 0:
                        visited[nr, nc] = True
                        stack.append((nr, nc))

            if best is None or len(comp) > len(best):
                best = comp

    if not best:
        return None

    rows = [r for r, _ in best]
    cols = [c for _, c in best]
    return min(rows), max(rows), min(cols), max(cols)

def all_nonzero_connected_components(x):
    h, w = x.shape
    visited = np.zeros((h, w), dtype=bool)
    components = []

    for r in range(h):
        for c in range(w):
            if visited[r, c] or x[r, c] == 0:
                continue

            stack = [(r, c)]
            visited[r, c] = True
            comp = []

            while stack:
                cr, cc = stack.pop()
                comp.append((cr, cc))
                for nr, nc in neighbors4(cr, cc, h, w):
                    if not visited[nr, nc] and x[nr, nc] != 0:
                        visited[nr, nc] = True
                        stack.append((nr, nc))

            components.append(comp)

    return components

def recolor_cropped_shape_from_clue_pairs(x):
        bbox = largest_nonzero_component_bbox(x)
        if bbox is None:
            return None

        r0, r1, c0, c1 = bbox
        cropped = x[r0:r1 + 1, c0:c1 + 1].copy()
        cropped_colors = {int(c) for c in np.unique(cropped) if c != 0}

        mapping = {}
        for comp in all_nonzero_connected_components(x):
            if len(comp) != 2:
                continue

            if all(r0 <= r <= r1 and c0 <= c <= c1 for r, c in comp):
                continue

            cells = sorted(comp, key=lambda rc: (rc[0], rc[1]))
            (ra, ca), (rb, cb) = cells

            if abs(ra - rb) + abs(ca - cb) != 1:
                continue

            color_a = int(x[ra, ca])
            color_b = int(x[rb, cb])
            if color_a == color_b:
                continue

            a_in = color_a in cropped_colors
            b_in = color_b in cropped_colors

            if a_in and not b_in:
                source, target = color_a, color_b
            elif b_in and not a_in:
                source, target = color_b, color_a
            elif ra == rb and abs(ca - cb) == 1:
                left, right = sorted(cells, key=lambda rc: rc[1])
                target = int(x[left[0], left[1]])
                source = int(x[right[0], right[1]])
            elif ca == cb and abs(ra - rb) == 1:
                top, bottom = sorted(cells, key=lambda rc: rc[0])
                target = int(x[top[0], top[1]])
                source = int(x[bottom[0], bottom[1]])
            else:
                continue

            mapping[source] = target

        if not mapping:
            return None

        changed = False
        for source, target in mapping.items():
            mask = cropped == source
            if np.any(mask):
                cropped[mask] = target
                changed = True

        return cropped if changed else None

def unique_orientations(piece):
    variants = []
    seen = set()

    candidates = [
        piece,
        np.rot90(piece, 1),
        np.rot90(piece, 2),
        np.rot90(piece, 3),
        np.fliplr(piece),
        np.flipud(piece),
        np.rot90(np.fliplr(piece), 1),
        np.rot90(np.flipud(piece), 1),
    ]

    for cand in candidates:
        key = tuple(tuple(int(v) for v in row) for row in cand.tolist())
        if key in seen:
            continue
        seen.add(key)
        variants.append(cand)

    return variants

def fit_pieces_into_base_slots(x):
        h, w = x.shape
        all_components = all_nonzero_components(x)
        if len(all_components) < 2:
            return None

        base_color = None
        base_comp = None
        best_score = None
        for color, comp in all_components:
            rows = [r for r, _ in comp]
            if max(rows) != h - 1:
                continue
            score = (len(comp), color)
            if best_score is None or score > best_score:
                best_score = score
                base_color = color
                base_comp = comp

        if base_comp is None:
            return None

        base_set = set(base_comp)
        top_row = min(r for r, _ in base_comp)
        if top_row == 0:
            return None

        min_col = min(c for _, c in base_comp)
        max_col = max(c for _, c in base_comp)

        out = np.zeros_like(x)
        for r, c in base_comp:
            out[r, c] = base_color

        slots = []
        c = min_col
        while c <= max_col:
            if x[top_row, c] != 0:
                c += 1
                continue

            c0 = c
            while c <= max_col and x[top_row, c] == 0:
                c += 1
            c1 = c - 1

            if top_row - 1 < 0:
                return None
            if any(x[top_row - 1, cc] != 0 for cc in range(c0, c1 + 1)):
                return None

            slots.append((c0, c1))

        pieces = []
        for color, comp in all_components:
            if color == base_color and comp == base_comp:
                continue
            rows = [r for r, _ in comp]
            cols = [c for _, c in comp]
            r0, r1 = min(rows), max(rows)
            c0, c1 = min(cols), max(cols)
            piece = np.zeros((r1 - r0 + 1, c1 - c0 + 1), dtype=x.dtype)
            for rr, cc in comp:
                piece[rr - r0, cc - c0] = color
            pieces.append((color, comp, piece))

        changed = False
        pieces.sort(key=lambda item: -len(item[1]))
        slots = sorted(slots, key=lambda span: span[1] - span[0] + 1)
        used_pieces = set()

        for c0, c1 in slots:
            slot_w = c1 - c0 + 1
            matched = False

            for piece_idx, (color, comp, piece) in enumerate(pieces):
                if piece_idx in used_pieces:
                    continue

                for oriented in unique_orientations(piece):
                    occ = oriented != 0
                    oh, ow = occ.shape
                    if oh != 2 or ow != slot_w:
                        continue
                    if not np.all(occ):
                        continue

                    for dr in range(2):
                        for dc in range(slot_w):
                            out[top_row - 1 + dr, c0 + dc] = int(oriented[dr, dc])
                    used_pieces.add(piece_idx)
                    changed = True
                    matched = True
                    break

                if matched:
                    break

        return out if changed else None

def mosaic_rot180_fliplr_bands(x):
    if x.shape != (3, 3):
        return None

    rot180 = np.rot90(x, 2)
    flipud = np.flipud(x)
    fliplr = np.fliplr(x)

    top = np.hstack([rot180, flipud, rot180])
    middle = np.hstack([fliplr, x, fliplr])
    bottom = np.hstack([rot180, flipud, rot180])
    return np.vstack([top, middle, bottom])

def overlay_split_panels_left_priority(x):
    h, w = x.shape
    if w < 3:
        return None

    sep_candidates = []
    for c in range(w):
        col = x[:, c]
        if np.all(col == col[0]) and col[0] != 0:
            sep_candidates.append(c)
    if not sep_candidates:
        return None

    sep_options = [c for c in sep_candidates if c > 0 and c + 1 < w and c == w - c - 1]
    if len(sep_options) != 1:
        return None
    sep = sep_options[0]
    left = x[:, :sep]
    right = x[:, sep + 1:]
    if left.shape != right.shape:
        return None

    out = left.copy()
    right_mask = right != 0
    left_zero_mask = left == 0
    if np.array_equal(right_mask, left_zero_mask):
        out[right_mask] = right[right_mask]
    return out

def mirror_attach_inside_8_border(x):
        out = x.copy()
        changed = False
        h, w = x.shape

        for comp in connected_components_of_color(x, 8):
            comp_set = set(comp)

            rows = [r for r, _ in comp]
            cols = [c for _, c in comp]
            border_h = max(rows) - min(rows) + 1
            border_w = max(cols) - min(cols) + 1

            reachable = np.zeros((h, w), dtype=bool)
            stack = []

            for r in range(h):
                for c in [0, w - 1]:
                    if (r, c) not in comp_set and not reachable[r, c]:
                        reachable[r, c] = True
                        stack.append((r, c))
            for c in range(w):
                for r in [0, h - 1]:
                    if (r, c) not in comp_set and not reachable[r, c]:
                        reachable[r, c] = True
                        stack.append((r, c))

            while stack:
                r, c = stack.pop()
                for nr, nc in neighbors4(r, c, h, w):
                    if (nr, nc) in comp_set or reachable[nr, nc]:
                        continue
                    reachable[nr, nc] = True
                    stack.append((nr, nc))

            visited = np.zeros((h, w), dtype=bool)
            for r in range(h):
                for c in range(w):
                    if (r, c) in comp_set or reachable[r, c] or visited[r, c]:
                        continue

                    region = []
                    region_stack = [(r, c)]
                    visited[r, c] = True

                    while region_stack:
                        cr, cc = region_stack.pop()
                        region.append((cr, cc))
                        for nr, nc in neighbors4(cr, cc, h, w):
                            if (nr, nc) in comp_set or reachable[nr, nc] or visited[nr, nc]:
                                continue
                            visited[nr, nc] = True
                            region_stack.append((nr, nc))

                    object_cells = [(rr, cc) for rr, cc in region if x[rr, cc] != 0 and x[rr, cc] != 8]
                    if not object_cells:
                        continue

                    reg_rows = [rr for rr, _ in region]
                    reg_cols = [cc for _, cc in region]
                    r0, r1 = min(reg_rows), max(reg_rows)
                    c0, c1 = min(reg_cols), max(reg_cols)

                    if border_w >= border_h:
                        center_sum = c0 + c1
                        for rr, cc in object_cells:
                            mirror_c = center_sum - cc
                            if (rr, mirror_c) in region and out[rr, mirror_c] == 0:
                                out[rr, mirror_c] = int(x[rr, cc])
                                changed = True
                    else:
                        center_sum = r0 + r1
                        for rr, cc in object_cells:
                            mirror_r = center_sum - rr
                            if (mirror_r, cc) in region and out[mirror_r, cc] == 0:
                                out[mirror_r, cc] = int(x[rr, cc])
                                changed = True

        return out if changed else None
#################### Milestones D #####################

#################### Milestones D #####################
rulesD = [xor_top_bottom_masks_to_six,
        expand_single_two_to_v_with_inner_diagonals,
        marker_frame_to_small_staircase,
        complete_missing_panel_by_separator_mirroring,
        trace_threes_between_single_one_and_two,
        surround_holey_ones_with_twos_and_fill_inner_edge_with_threes,
        fill_closed_barrier_with_majority_color,
        count_panel_blocks_to_staircase,
        recolor_cropped_shape_from_clue_pairs,
        fit_pieces_into_base_slots,
        mosaic_rot180_fliplr_bands,
        overlay_split_panels_left_priority,
        mirror_attach_inside_8_border,]
#################### Milestones D #####################