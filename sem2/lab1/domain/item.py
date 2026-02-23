from typing import TypedDict, Optional
from domain.deadline import Deadline

class Item(TypedDict):
    num: int
    task: str
    deadline: Deadline 
    notes: Optional[str]