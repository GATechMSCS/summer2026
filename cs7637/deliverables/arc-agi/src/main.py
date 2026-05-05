from pathlib import Path
from task_io import load_tasks, grid_to_text
from solver import SimpleArcSolver


def run(folder):
    solver = SimpleArcSolver()
    tasks = load_tasks(folder)
    for task in tasks:
        pred, hyps = solver.solve(task)
        print(f"Task: {task.task_id}")
        print(f"Valid hypotheses: {[h.name for h in hyps[:10]]}")
        if pred is not None:
            print(grid_to_text(pred))
        print("-" * 40)


if __name__ == "__main__":
    run(Path("data"))
