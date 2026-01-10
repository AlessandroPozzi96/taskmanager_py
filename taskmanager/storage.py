import json
from pathlib import Path
from typing import List


from models import Task, TaskStatus

class TaskRepository:
    def __init__(self, file_path: Path):
        self.file_path = file_path
    
    def load(self) -> List[Task]:
        if not self.file_path.exists():
            return []
        
        with self.file_path.open("r", encoding="utf-8") as f:
            raw_tasks = json.load(f)

        return [self._deserialize(task) for task in raw_tasks]

    def save(self, tasks: List[Task]) -> None:
        with self.file_path.open("w", encoding="utf-8") as f:
            json.dump(
                [self._serialize(task) for task in tasks],
                f,
                indent=2,
                ensure_ascii=False,
            )

    @staticmethod
    def _serialize(task: Task) -> dict:
        return {
            "id": task.id,
            "title": task.title,
            "status": task.status.value
        }
    
    @staticmethod
    def _deserialize(data: dict) -> Task:
        return Task(
            id = data["id"],
            title = data["title"],
            status = TaskStatus(data["status"]),
        )

