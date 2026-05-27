import numpy as np

from ArcProblem import ArcProblem
from ArcData import ArcData
from ArcSet import ArcSet
import milestoneAB as mab
# import milestoneC as msc
# import milestoneD as md
import hidden_cases as hc


class ArcAgent:

    def __init__(self):
        """
        You may add additional variables to this init method. Be aware that it gets called only once
        and then the make_predictions method will get called several times.
        """
        pass

    def make_predictions(self, arc_problem: ArcProblem) -> list[np.ndarray]:
        """
        Write the code in this method to solve the incoming ArcProblem.
        Your agent will receive 1 problem at a time.

        You can add up to THREE (3) the predictions to the
        predictions list provided below that you need to
        return at the end of this method.

        In the Autograder, the test data output in the arc problem will be set to None
        so your agent cannot peek at the answer (even on the public problems).

        Also, if you return more than 3 predictions in the list it
        is considered an ERROR and the test will be automatically
        marked as INCORRECT.
        """

        predictions: list[np.ndarray] = list()
        seen = set()

        train = [(ex.get_input_data().data(), ex.get_output_data().data())
                 for ex in arc_problem.training_set()]
        testI = arc_problem.test_set().get_input_data().data()

        # '''
        # The next 2 lines are only an example of how to populate the predictions list.
        # This will just be an empty answer the size of the input data;
        # delete it before you start adding your own predictions.
        # '''
        # output = np.zeros_like(arc_problem.test_set().get_input_data().data())
        # predictions.append(output)

        ############### HELPERS ###############
        def add(arr):
            if arr is None or len(predictions) >= 3:
                return
            key = (arr.shape, tuple(arr.flatten()))
            if key not in seen:
                seen.add(key)
                predictions.append(arr)

        def fits(fn):
            for x, y in train:
                out = fn(x)
                if out is None or out.shape != y.shape or not np.array_equal(out, y):
                    return False
            return True

        def bbox_nonzero(grid):
            pts = np.argwhere(grid != 0)
            if len(pts) == 0:
                return None
            r0, c0 = pts.min(axis=0)
            r1, c1 = pts.max(axis=0)
            return r0, r1, c0, c1

        def crop_nonzero(grid):
            b = bbox_nonzero(grid)
            if b is None:
                return grid.copy()
            r0, r1, c0, c1 = b
            return grid[r0:r1 + 1, c0:c1 + 1]

        def color_remap(grid):
            mapping = {}
            for x, y in train:
                if x.shape != y.shape:
                    return None
                for a, b in zip(x.flatten(), y.flatten()):
                    if a in mapping and mapping[a] != b:
                        return None
                    mapping[a] = b
            out = grid.copy()
            for a, b in mapping.items():
                out[grid == a] = b
            return out

        def overlap_split(grid):
            cols = grid.shape[1]
            for c in range(cols):
                vals = np.unique(grid[:, c])
                if len(vals) == 1:
                    left, right = grid[:, :c], grid[:, c + 1:]
                    if left.shape == right.shape:
                        return ((left != 0) & (right != 0)).astype(int) * 2
            return None
        ############### HELPERS ###############

        rules = [
            lambda x: x.copy(),
            lambda x: np.rot90(x, 1),
            lambda x: np.rot90(x, 2),
            lambda x: np.rot90(x, 3),
            np.fliplr,
            np.flipud,
            crop_nonzero,
            color_remap,
            overlap_split,]

        for rule in rules:
            if fits(rule):
                add(rule(testI))

        add(testI.copy())
        add(crop_nonzero(testI))
        add(np.zeros_like(testI))

        return predictions[:3]