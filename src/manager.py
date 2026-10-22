import json
import os
from typing import List, Optional
from src.task import Task

class TaskManager:
    def __init__(self, storage_path: str = "tasks.json"):
        self.storage_path = storage_path
        self.tasks: List[Task] = []
        self._load()

    def _load(self) -> None:
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.tasks = [Task.from_dict(item) for item in data]
            except (json.JSONDecodeError, OSError):
                self.tasks = []

    def _save(self) -> None:
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in self.tasks], f, indent=2)

    def add_task(self, title: str, priority: str = "medium") -> Task:
        clean_title = title.strip()
        next_id = max([t.id for t in self.tasks], default=0) + 1
        task = Task(id=next_id, title=clean_title, priority=priority)
        self.tasks.append(task)
        self._save()
        return task

    def list_tasks(self, include_completed: bool = True) -> List[Task]:
        if include_completed:
            return list(self.tasks)
        return [t for t in self.tasks if not t.completed]

    def complete_task(self, task_id: int) -> Optional[Task]:
        for t in self.tasks:
            if t.id == task_id:
                t.completed = True
                self._save()
                return t
        return None

    def delete_task(self, task_id: int) -> bool:
        initial_len = len(self.tasks)
        self.tasks = [t for t in self.tasks if t.id != task_id]
        if len(self.tasks) < initial_len:
            self._save()
            return True
        return False
