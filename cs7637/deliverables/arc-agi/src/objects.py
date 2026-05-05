from grid_ops import bounding_box

class ArcObject:
    def __init__(self, color, cells):
        self.color = color
        self.cells = cells
        self.box = bounding_box(cells)
        self.area = len(cells)

    def summary(self):

        r1, c1, r2, c2 = self.box

        return {"color": self.color,
                "area": self.area,
                "bbox": (r1, c1, r2, c2),}
