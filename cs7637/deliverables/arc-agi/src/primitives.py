from copy import deepcopy


def recolor(grid, old, new):
    out = deepcopy(grid)
    for r, row in enumerate(out):
        for c, val in enumerate(row):
            if val == old:
                out[r][c] = new
    return out


def flip_horizontal(grid):
    return [list(reversed(row)) for row in grid]


def flip_vertical(grid):
    return list(reversed(grid))


def rotate_right(grid):
    return [list(row) for row in zip(*grid[::-1])]
