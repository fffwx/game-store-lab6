"""Репозиторій для роботи з покупками"""

from typing import List, Optional
from src.models.purchase import Purchase


class PurchaseRepository:
    """Репозиторій для управління даними покупок"""

    def __init__(self):
        self._purchases: dict[int, Purchase] = {}
        self._next_id = 1

    def add(self, purchase: Purchase) -> Purchase:
        """Додає нову покупку"""
        if purchase.id == 0:
            purchase.id = self._next_id
            self._next_id += 1
        self._purchases[purchase.id] = purchase
        return purchase

    def find_by_id(self, purchase_id: int) -> Optional[Purchase]:
        """Знаходить покупку за ID"""
        return self._purchases.get(purchase_id)

    def find_by_user(self, user_id: int) -> List[Purchase]:
        """Знаходить всі покупки користувача"""
        return [
            purchase for purchase in self._purchases.values()
            if purchase.user_id == user_id and not purchase.is_returned
        ]

    def find_by_game(self, game_id: int) -> List[Purchase]:
        """Знаходить всі покупки гри"""
        return [
            purchase for purchase in self._purchases.values()
            if purchase.game_id == game_id
        ]

    def find_user_game_purchase(self, user_id: int, game_id: int) -> Optional[Purchase]:
        """Знаходить покупку гри конкретним користувачем"""
        for purchase in self._purchases.values():
            if purchase.user_id == user_id and purchase.game_id == game_id and not purchase.is_returned:
                return purchase
        return None

    def update(self, purchase: Purchase) -> Purchase:
        """Оновлює інформацію про покупку"""
        if purchase.id in self._purchases:
            self._purchases[purchase.id] = purchase
        return purchase

    def find_all(self) -> List[Purchase]:
        """Повертає всі покупки"""
        return list(self._purchases.values())

    def clear(self):
        """Очищує репозиторій (для тестів)"""
        self._purchases.clear()
        self._next_id = 1
