from dataclasses import dataclass
from datetime import datetime

@dataclass
class ReminderRecord:
    user_id: str
    query_txt: str
    reminder_txt: str
    reminder_date: datetime
