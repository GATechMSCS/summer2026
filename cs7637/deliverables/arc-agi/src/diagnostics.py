
def same_grid(a, b):
    return a == b

def cell_diff(a, b):

    diffs = []
    rows = max(len(a), len(b))
    cols = max(len(a[0]), len(b[0])) if a and b else 0
    for r in range(rows):
        for c in range(cols):
            av = a[r][c] if r < len(a) and c < len(a[0]) else None
            bv = b[r][c] if r < len(b) and c < len(b[0]) else None
            if av != bv:
                diffs.append((r, c, av, bv))
    return diffs
