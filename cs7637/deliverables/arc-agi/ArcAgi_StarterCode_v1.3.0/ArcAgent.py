from grid_utils import (split_line,
                        find_them,
                        detect_holes_and_border)
from ArcProblem import ArcProblem
from milestoneAB import rulesAB
from milestoneC import rulesC
from milestoneD import rulesD
import numpy as np

class ArcAgent:

    def __init__(self):
        """
        You may add additional variables to this init method. Be aware that it gets called only once
        and then the make_predictions method will get called several times.
        """

        # fine for now but need a list with all milestone rules for final part.
        self.rule_bank = rulesAB + rulesC + rulesD
        #self.rule_bank = rulesD
        self.builder_bank = (self._build_color_filter_rule,
                             self._build_or_panel_rule,
                             self._build_marker_shape_rule,
                             self._build_role_color_rule,)
        self.logic_gates = ("and", "or", "xor", "nor")

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

        train = [(ex.get_input_data().data(), ex.get_output_data().data())
                 for ex in arc_problem.training_set()]
        test_grid = arc_problem.test_set().get_input_data().data()

        # '''
        # The next 2 lines are only an example of how to populate the predictions list.
        # This will just be an empty answer the size of the input data;
        # delete it before you start adding your own predictions.
        # '''
        # output = np.zeros_like(arc_problem.test_set().get_input_data().data())
        # predictions.append(output)

        for fn in self._candidate_functions(train):
            self._push_unique(predictions, fn(test_grid))
            if len(predictions) >= 3:
                break

        return predictions[:3]

    def _candidate_functions(self, train):

        for rule in self.rule_bank:
            if self._matches_training(rule, train):
                yield rule

        for builder in self.builder_bank:
            rule = builder(train)
            if rule is not None:
                yield rule

        for gate in self.logic_gates:
            rule = self._build_panel_mask_rule(train, gate)
            if rule is not None:
                yield rule

    def _push_unique(self, predictions, pred):

        if pred is None:
            return
        if any(np.array_equal(pred, seen) for seen in predictions):
            return
        predictions.append(pred)

    def _matches_training(self, fn, train):

        try:
            return all((pred := fn(inp)) is not None and np.array_equal(pred, out)
                    for inp, out in train)
        except Exception:
            return False

    def _nonzero_colors(self, grid: np.ndarray):

        return [int(color) for color in np.unique(grid) if color != 0]

    def _single_output_color(self, grid: np.ndarray):

        vals = self._nonzero_colors(grid)
        return vals[0] if len(vals) == 1 else None

    def _marker_signature(self, grid: np.ndarray):

        ones = np.argwhere(grid == 1)
        if len(ones) == 0:
            return None

        colors = [int(c) for c in np.unique(grid) if c not in (0, 1)]
        if len(colors) != 1:
            return None
        color = colors[0]

        blobs = np.argwhere(grid == color)
        if len(blobs) == 0:
            return None

        row0, row1 = ones[:, 0].min(), ones[:, 0].max()
        col0, col1 = ones[:, 1].min(), ones[:, 1].max()

        bins: dict[tuple[int, int], int] = {}
        for row, col in blobs:
            vert_dist = int(min(abs(row - row0), abs(row - row1)))
            horiz_dist = int(min(abs(col - col0), abs(col - col1)))
            bins[(vert_dist, horiz_dist)] = bins.get((vert_dist, horiz_dist), 0) + 1

        return color, tuple(sorted(bins.items()))

    def _build_marker_shape_rule(self, train):

        prototypes = []

        for inp, out in train:
            sig = self._marker_signature(inp)
            if sig is None:
                return None

            color, bins = sig
            out_color = self._single_output_color(out)
            if out_color != color:
                return None

            pattern = (out != 0).astype(np.uint8)
            if not np.any(pattern):
                return None

            prototypes.append((bins, pattern))

        if not prototypes:
            return None

        def distance(bins, items):

            bin_dict = dict(bins)
            item_dic = dict(items)
            keys = set(bin_dict) | set(item_dic)
            return sum(abs(bin_dict.get(key, 0) - item_dic.get(key, 0)) for key in keys)

        def apply(grid: np.ndarray):

            sig = self._marker_signature(grid)
            if sig is None:
                return None

            color, bins = sig
            best_pattern = min(prototypes, key=lambda item: distance(bins, item[0]))[1]

            out_grid = np.zeros_like(best_pattern, dtype=grid.dtype)
            out_grid[best_pattern != 0] = color
            return out_grid

        return apply

    def _build_color_filter_rule(self, train):

        learned = None

        for inp, out in train:
            out_color = self._single_output_color(out)
            if out_color is None:
                return None

            match = None
            for src in self._nonzero_colors(inp):
                candidate = np.zeros_like(inp)
                candidate[inp == src] = out_color
                if np.array_equal(candidate, out):
                    match = (src, out_color)
                    break

            if match is None:
                return None
            if learned is None:
                learned = match
            elif learned != match:
                return None

        if learned is None:
            return None

        src_color, dst_color = learned

        def apply(grid: np.ndarray):

            out_grid = np.zeros_like(grid)
            out_grid[grid == src_color] = dst_color
            return out_grid

        return apply

    def _build_or_panel_rule(self, train):

        for inp, out in train:
            panels = split_line(inp)
            if panels is None:
                return None

            left, right = panels
            if left.shape != right.shape or left.shape != out.shape:
                return None

            candidate = ((left != 0) | (right != 0)).astype(inp.dtype)
            if not np.array_equal(candidate, out):
                return None

        def apply(grid: np.ndarray):

            panels = split_line(grid)
            if panels is None:
                return None

            left, right = panels
            if left.shape != right.shape:
                return None

            return ((left != 0) | (right != 0)).astype(grid.dtype)

        return apply

    def _logic_gates(self, panel1: np.ndarray, panel2: np.ndarray, gate: str):

        gates = {"and": lambda x, y: (x != 0) & (y != 0),
                 "or": lambda x, y: (x != 0) | (y != 0),
                 "xor": lambda x, y: (x != 0) ^ (y != 0),
                 "nor": lambda x, y: (x == 0) & (y == 0)}
        get_gates = gates.get(gate)
        return None if get_gates is None else get_gates(panel1, panel2)

    def _build_panel_mask_rule(self, train, gate: str):

        painted_color = None

        for inp, out in train:
            panels = split_line(inp)
            if panels is None:
                return None

            panel1, panel2 = panels
            if panel1.shape != panel2.shape or panel1.shape != out.shape:
                return None

            mask = self._logic_gates(panel1, panel2, gate)
            if mask is None:
                return None

            non_zero = np.unique(out[out != 0])
            if len(non_zero) > 1:
                return None

            current_color = 1 if len(non_zero) == 0 else int(non_zero[0])
            candidate = np.zeros_like(panel1)
            candidate[mask] = current_color

            if not np.array_equal(candidate, out):
                return None

            if painted_color is None:
                painted_color = current_color
            elif painted_color != current_color:
                return None

        if painted_color is None:
            return None

        def apply(grid: np.ndarray):

            panels = split_line(grid)
            if panels is None:
                return None

            panel1, panel2 = panels
            if panel1.shape != panel2.shape:
                return None

            mask = self._logic_gates(panel1, panel2, gate)
            if mask is None:
                return None

            out_grid = np.zeros_like(panel1)
            out_grid[mask] = painted_color
            return out_grid

        return apply

    def _build_role_color_rule(self, train):

        if not train:
            return None

        learned = None

        for inp, out in train:
            inp_colors = [int(color) for color in np.unique(inp)]
            out_colors = [int(color) for color in np.unique(out)]

            bg = max(inp_colors, key=lambda c: int(np.sum(inp == c)))
            non_bg = [color for color in inp_colors if color != bg]
            if len(non_bg) != 1:
                return None
            shape = non_bg[0]

            added = [color for color in out_colors if color not in inp_colors]
            if len(added) not in (0, 2):
                return None
            if len(added) != 2:
                return None

            counts = sorted(((int(np.sum(out == color)), color) for color in added), reverse=True)
            outer, inner = counts[0][1], counts[1][1]

            current = (bg, shape, outer, inner)
            if learned is None:
                learned = current
            elif learned != current:
                return None

        if learned is None:
            return None

        bg, shape, outer, inner = learned

        def apply(grid: np.ndarray):

            out_grid = grid.copy()
            changed = False

            for color, cells in find_them(grid):
                if color != shape:
                    continue

                holes, border = detect_holes_and_border(grid, cells, bg, shape)

                for r, c in border:
                    if out_grid[r, c] == bg:
                        out_grid[r, c] = outer
                        changed = True

                for hole in holes:
                    for row, col in hole:
                        if out_grid[row, col] == bg:
                            out_grid[row, col] = inner
                            changed = True

            return out_grid if changed else None

        return apply