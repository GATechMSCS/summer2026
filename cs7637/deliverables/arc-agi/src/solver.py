from hypotheses import baseline_hypotheses
from diagnostics import same_grid


class SimpleArcSolver:

    def __init__(self):

        self.hypotheses = baseline_hypotheses()

    def fit(self, train_examples):

        valid = []
        for hyp in self.hypotheses:
            ok = True
            for ex in train_examples:
                if not same_grid(hyp.apply(ex["input"]), ex["output"]):
                    ok = False
                    break
            if ok:
                valid.append(hyp)

        return valid

    def solve(self, task):

        valid = self.fit(task.train)
        if not valid:
            return None, []
        hyp = valid[0]
        out = hyp.apply(task.test[0]["input"])

        return out, valid
