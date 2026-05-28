import numpy as np

from ArcProblem import ArcProblem
from ArcData import ArcData
from ArcSet import ArcSet
from milestoneAB import rulesAB
# from milestoneC import rulesC
# from milestoneD import rulesD
# from hidden_cases import rulesH


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

        for rule in rulesAB:
            if self._fit_training_data(train, rule):
                pred = rule(testI)
                self._append_if_new(predictions, pred)

        return predictions[:3]

    def _append_if_new(self, predictions, pred):
        if pred is None:
            return
        for p in predictions:
            if np.array_equal(p, pred):
                return
        predictions.append(pred)

    def _fit_training_data(self, xy_train, fn):
        for x_train, y_train in xy_train:
            preds = fn(x_train)
            if preds is None or not np.array_equal(preds, y_train):
                return False
        return True
