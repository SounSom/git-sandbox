from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Task:
    id: int
    title: str
    completed: bool = False

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(
            id=data["id"],
            title=data["title"],
            completed=data.get("completed", False)
        )
