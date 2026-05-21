from ArcData import ArcData
from ArcProblem import ArcProblem
from ArcSet import ArcSet
import numpy as np
import torch

class ArcAgent:
    def __init__(self):
        """
        model: Hugging Face model (loaded with LoRA if submitted)
        tokenizer: Hugging Face tokenizer
        """
        self.model = None
        self.tokenizer = None

    def set_model_and_tokenizer(self, model=None, tokenizer=None):
        """
        Loads the model and the tokenizer this agent will use.
        
        Students do not need to call this as the Autograder will load these for you
        with your training data already applied.
        """
        self.model = model
        self.tokenizer = tokenizer

    def make_predictions(self, problem: ArcProblem) -> list[np.ndarray]:
        """
        Generate up to 3 predicted grids (numpy arrays).
        Returns list of np.ndarray (empty array if invalid/no prediction).
        """

        predictions = []

        return predictions[:3]  # wll return the first 3 predictions only
