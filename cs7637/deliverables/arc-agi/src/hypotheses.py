from primitives import recolor, flip_horizontal, flip_vertical, rotate_right


class Hypothesis:
    def __init__(self, name, fn):
        self.name = name
        self.fn = fn

    def apply(self, grid):
        return self.fn(grid)


def baseline_hypotheses():
    return [
        Hypothesis("identity", lambda g: g),
        Hypothesis("flip_horizontal", flip_horizontal),
        Hypothesis("flip_vertical", flip_vertical),
        Hypothesis("rotate_right", rotate_right),
    ] + [
        Hypothesis(f"recolor_{old}_{new}", lambda g, old=old, new=new: recolor(g, old, new))
        for old in range(10)
        for new in range(10)
        if old != new
    ]
