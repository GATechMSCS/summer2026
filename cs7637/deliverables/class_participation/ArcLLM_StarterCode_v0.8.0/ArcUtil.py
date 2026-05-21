import numpy as np

def grid_to_string(grid):
    """
    Compact format to reduce token count: comma-separated rows.
    Example: [[0,1],[2,3]] → [0,1],[2,3]
    """
    if grid.size == 0:
        return "[]"
    return '[' + ','.join('[' + ','.join(map(str, row)) + ']' for row in grid) + ']'

def parse_generated_grid(generated_text):
    """
    Extract a 2D grid from generated text. Returns np.ndarray or empty array.
    """
    # Look for common patterns: after "Output:", or just the first list-like block
    start_idx = generated_text.find("Output:")
    if start_idx == -1:
        start_idx = 0
    text = generated_text[start_idx:].strip()

    # Extract first valid grid-like structure
    lines = [line.strip() for line in text.split('\n') if line.strip() and '[' in line]
    if not lines:
        return np.array([])

    grid_lines = []
    for line in lines:
        # Clean and parse numbers
        cleaned = ''.join(c for c in line if c.isdigit() or c in ',[]')
        if cleaned.startswith('[') and cleaned.endswith(']'):
            row_str = cleaned[1:-1]  # strip outer []
            row = [int(x) for x in row_str.split(',') if x.strip().isdigit()]
            if row:
                grid_lines.append(row)

    if not grid_lines:
        return np.array([])

    grid = np.array(grid_lines)
    if grid.ndim == 2 and np.all((grid >= 0) & (grid <= 9)):
        return grid
    return []

