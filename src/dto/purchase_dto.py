"""DTO для покупки"""

from dataclasses import dataclass


@dataclass
class PurchaseDTO:
    """Об'єкт передачі даних для покупки"""

    id: int
    user_id: int
    game_id: int
    purchase_date: str
    price_paid: float
    is_returned: bool

    @classmethod
    def from_purchase(cls, purchase):
        """Створює DTO з моделі Purchase"""
        return cls(
            id=purchase.id,
            user_id=purchase.user_id,
            game_id=purchase.game_id,
            purchase_date=purchase.purchase_date.strftime("%Y-%m-%d %H:%M"),
            price_paid=purchase.price_paid,
            is_returned=purchase.is_returned,
        )
