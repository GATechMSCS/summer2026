from collections import deque

def dims(grid):
    return len(grid), len(grid[0]) if grid else 0

def in_bounds(grid, r, c):
    rows, cols = dims(grid)
    return 0 <= r < rows and 0 <= c < cols

def neighbors4(r, c):
    return [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]

def connected_components(grid, background=None):
    rows, cols = dims(grid)
    seen = set()
    comps = []
    for r in range(rows):
        for c in range(cols):
            if (r, c) in seen:
                continue
            color = grid[r][c]
            if background is not None and color == background:
                continue
            q = deque([(r, c)])
            seen.add((r, c))
            cells = []
            while q:
                cr, cc = q.popleft()
                cells.append((cr, cc))
                for nr, nc in neighbors4(cr, cc):
                    if in_bounds(grid, nr, nc) and (nr, nc) not in seen and grid[nr][nc] == color:
                        seen.add((nr, nc))
                        q.append((nr, nc))
            comps.append({"color": color, "cells": cells})
    return comps

def bounding_box(cells):
    rs = [r for r, _ in cells]
    cs = [c for _, c in cells]
    return min(rs), min(cs), max(rs), max(cs)
