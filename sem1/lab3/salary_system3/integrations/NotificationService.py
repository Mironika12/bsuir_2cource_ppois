from typing import List, Dict, Any


class NotificationService:
    def __init__(self, service_id: str, channels: List[str], templates: Dict[str, str]):
        self.service_id: str = service_id
        self.channels: List[str] = channels
        self.templates: Dict[str, str] = templates
        self.sent_notifications: List[Dict[str, Any]] = []

    def notify(self, recipient: str, message: str, payslip: Any = None) -> bool:
        notification_record: Dict[str, Any] = {
            "recipient": recipient,
            "message": message,
            "payslip": payslip
        }
        self.sent_notifications.append(notification_record)
        return True

    def schedule(self, recipient: str, message: str, send_time: Any, payslip: Any = None) -> bool:
        scheduled_record: Dict[str, Any] = {
            "recipient": recipient,
            "message": message,
            "send_time": send_time,
            "payslip": payslip
        }
        self.sent_notifications.append(scheduled_record)
        return True
