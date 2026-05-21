import json
import os.path
import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

from ArcData import ArcData
from ArcProblem import ArcProblem
from ArcSet import ArcSet
from ArcAgent import ArcAgent


def load_arc_problems(path: str, problem_data: list[str]) -> list[ArcProblem]:
    problems: list[ArcProblem] = []
    for problem_name in problem_data:
        with open(os.path.join(path, problem_name)) as p:
            flat_data: dict[str, dict] = json.load(p)
            trn_data: list[ArcSet] = []
            for dt in flat_data['train']:
                d_input = ArcData(np.array(dt['input']))
                d_output = ArcData(np.array(dt['output']))
                trn_set: ArcSet = ArcSet(arc_input=d_input, arc_output=d_output)
                trn_data.append(trn_set)

            tst_data: list[ArcSet] = []
            for tst in flat_data['test']:
                t_input = ArcData(np.array(tst['input']))
                t_output = ArcData(np.array(tst['output']))
                tst_set: ArcSet = ArcSet(arc_input=t_input, arc_output=t_output)
                tst_data.append(tst_set)

            arc_problem = ArcProblem(problem_name[:-5], trn_data, tst_data[0])
            problems.append(arc_problem)
    return problems


def run_training_data(agent: ArcAgent, arc_problems: list[ArcProblem]) -> dict[ArcProblem, tuple[bool, list]]:
    train_ans_dict: dict[ArcProblem, tuple[bool, list]] = {}
    for trn_problem in arc_problems:
        preds: list[np.ndarray] = agent.make_predictions(trn_problem)

        correct = False
        if len(preds) <= 3:
            for prediction in preds:
                answer = trn_problem.test_set().get_output_data().data()
                correct = np.array_equal(answer, prediction)
                if correct:
                    break

        train_ans_dict[trn_problem] = (correct, preds)
    return train_ans_dict


def load_llm_and_lora(model_name: str, lora_folder: str = None):
    """
    Load the requested base model + optional LoRA.
    """
    model_map = {
        "microsoft/Phi-4-mini-instruct": "/autograder/models/phi-4",
        "ministral/Ministral-3-3B-Instruct-2512": "/autograder/models/ministral3",
        "qwen/Qwen2.5-3B-Instruct": "/autograder/models/qwen2_5",
        "huggingface/SmolLM3-3B": "/autograder/models/smollm3"
    }

    if model_name not in model_map:
        raise ValueError(f"Invalid model name: {model_name}. Allowed: {list(model_map.keys())}")

    model_folder = model_map[model_name]
    print(f"Loading base model: {model_name} from {model_folder}")

    tokenizer = AutoTokenizer.from_pretrained(model_folder, trust_remote_code=True)

    from transformers import BitsAndBytesConfig
    quant_config = BitsAndBytesConfig(load_in_8bit=True)

    model = AutoModelForCausalLM.from_pretrained(
        model_folder,
        quantization_config=quant_config,
        device_map="auto",
        trust_remote_code=True,
        torch_dtype=torch.float16
    )

    if lora_folder and os.path.exists(lora_folder):
        print(f"Applying LoRA from: {lora_folder}")
        model = PeftModel.from_pretrained(model, lora_folder)
        model = model.merge_and_unload()

    return model, tokenizer


if __name__ == "__main__":
    # === Check for model_name.txt ===
    MODEL_NAME_FILE = "model_name.txt"
    MODEL_NAME = None
    LORA_FOLDER = "./my_lora"  # set to 'None' to skip

    if os.path.exists(MODEL_NAME_FILE):
        with open(MODEL_NAME_FILE, 'r') as f:
            lines = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
        
        if lines:
            MODEL_NAME = lines[0]  # Take the first uncommented line
            print(f"Detected model: {MODEL_NAME}")
        else:
            print("model_name.txt found but all lines commented → running without LLM")
    else:
        print("No model_name.txt found → running without LLM")

    # Load model + LoRA only if valid name was found
    model = None
    tokenizer = None
    if MODEL_NAME:
        try:
            model, tokenizer = load_llm_and_lora(MODEL_NAME, LORA_FOLDER if os.path.exists(LORA_FOLDER) else None)
        except Exception as e:
            print(f"Failed to load model/LoRA: {e}")
            print("Falling back to non-LLM mode")

    # Create agent and inject model/tokenizer (mimics Gradescope)
    arc_agent = ArcAgent()
    arc_agent.set_model_and_tokenizer(model=model, tokenizer=tokenizer)

    # === Choose milestone folder ===
    problems_path = os.path.join(problems)
    problem_data: list[str] = os.listdir(milestone_path)

    arc_problems: list[ArcProblem] = load_arc_problems(problems_path, problem_data)

    # Run evaluation
    problem_data_set = run_training_data(arc_agent, arc_problems)

    # Save results to CSV
    results_file = open('ArcLLM_Results.csv', 'w')
    results_file.write("Problem Name, Correct, Correct Answer, Prediction 1, Prediction 2, Prediction 3\n")
    for m_answer_set in problem_data_set.keys():
        m_correct, predictions = problem_data_set[m_answer_set]
        m_cor_ans = m_answer_set.test_set().get_output_data().data().tolist()
        results_file.write(f'{m_answer_set.problem_name()},'
                             f'{m_correct},'
                             f'"{m_cor_ans}",')
        if len(predictions) == 0:
            results_file.write("empty\n")
            continue
        for idx, pred in enumerate(predictions, 1):
            if len(predictions) == idx:
                results_file.write(f'"{pred.tolist()}"\n')
            else:
                milestone_file.write(f'"{pred.tolist()}",')

    results_file.close()
    print("Results saved to ArcLLM_Results.csv")