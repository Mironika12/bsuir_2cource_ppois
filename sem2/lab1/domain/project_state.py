from enum import Enum, auto

class ProjectState(Enum):
    CREATED = auto()
    TOPIC_SELECTED = auto()
    PLANNING = auto()
    RESEARCH = auto()
    WRITING = auto()
    CONSULTING = auto()
    SUBMITTED = auto()