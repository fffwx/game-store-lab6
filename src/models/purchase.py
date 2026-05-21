"""Модель покупки"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Purchase:
    """Модель покупки гри"""

    id: int
    user_id: int
    game_id: int
    purchase_date: datetime
    price_paid: float
    is_returned: bool = False
    return_date: Optional[datetime] = None

    def days_since_purchase(self) -> int:
        """Кількість днів з моменту покупки"""
        delta = datetime.now() - self.purchase_date
        return delta.days
