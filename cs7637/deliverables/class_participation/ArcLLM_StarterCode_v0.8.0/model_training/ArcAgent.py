from ArcProblem import ArcProblem
from ArcUtil import parse_generated_grid, grid_to_string
import numpy as np

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
        if self.model is None or self.tokenizer is None:
            # Non-LLM fallback
            return []

        # Build compact few-shot prompt (limit to 3 examples max)
        prompt = "ARC task examples:\n"
        for i, train_set in enumerate(problem.training_set()[:3]):
            inp = train_set.get_input_data().data().tolist()
            out = train_set.get_output_data().data().tolist()
            prompt += f"Ex {i+1} Input: {grid_to_string(np.array(inp))}\n"
            prompt += f"Output: {grid_to_string(np.array(out))}\n\n"

        test_grid = problem.test_set().get_input_data().data().tolist()
        prompt += f"Test Input: {grid_to_string(np.array(test_grid))}\n"
        prompt += "Output (list of lists, only numbers 0-9):"

        try:
            # Tokenize with truncation safety (max 3800 tokens)
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=3800
            )
            input_ids = inputs["input_ids"].to(self.model.device)
            attention_mask = inputs["attention_mask"].to(self.model.device)

            # Generate with optimized parameters
            outputs = self.model.generate(
                input_ids,
                attention_mask=attention_mask,
                max_new_tokens=384,
                temperature=0.4,
                top_p=0.92,
                top_k=40,
                repetition_penalty=1.08,
                do_sample=True,
                num_return_sequences=3,
                pad_token_id=self.tokenizer.eos_token_id,
                eos_token_id=self.tokenizer.eos_token_id
            )

            predictions = []
            for i in range(outputs.shape[0]):
                generated_text = self.tokenizer.decode(outputs[i], skip_special_tokens=True)
                # Trim prompt prefix
                generated_text = generated_text[len(prompt):].strip()

                grid = parse_generated_grid(generated_text)
                if grid.size > 0 and grid.ndim == 2 and np.all((grid >= 0) & (grid <= 9)):
                    predictions.append(grid)

            # Ensure up to 3 predictions (pad with empty if needed)
            while len(predictions) < 3:
                predictions.append(np.array([]))

            return predictions[:3]

        except Exception as e:
            # Log error but return fallback
            print(f"Generation failed: {e}")
            return []