from dataclasses import dataclass
from enum import Enum

class TaskStatus(Enum):
    TODO = "TODO"
    DONE = "DONE"

@dataclass
class Task:
    id:int
    title:str
    status:TaskStatus = TaskStatus.TODO