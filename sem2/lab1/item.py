from typing import TypedDict, Optional

class Item(TypedDict):
    num: int
    task: str
    deadline: Deadline 
    notes: Optional[str]