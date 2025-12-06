from typing import List


class OnboardingChecklist:
    def __init__(self, checklist_id: str, items: List[str], employee_id: str):
        self.checklist_id: str = checklist_id
        self.items: List[str] = items
        self.employee_id: str = employee_id
        self.completed_items: List[str] = []

    def mark_complete(self, item: str) -> bool:
        if item in self.items and item not in self.completed_items:
            self.completed_items.append(item)
            return True
        return False

    def pending_items(self) -> List[str]:
        return [item for item in self.items if item not in self.completed_items]
