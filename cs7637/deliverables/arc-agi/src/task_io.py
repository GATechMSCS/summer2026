from pathlib import Path
import json

class ArcTask:

    def __init__(self, task_id, train, test):

        self.task_id = task_id
        self.train = train
        self.test = test

def load_task(path):

    path = Path(path)
    data = json.loads(path.read_text())

    return ArcTask(path.stem, data.get("train", []), data.get("test", []))

def load_tasks(folder):

    folder = Path(folder)

    return [load_task(p) for p in sorted(folder.glob("*.json"))]

def grid_to_text(grid):

    return "\n".join(" ".join(str(cell) for cell in row) for row in grid)
