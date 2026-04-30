from dataclasses import dataclass
from typing import List


@dataclass
class User:
    """Модель користувача магазину ігор"""
    id: int
    username: str
    email: str
    password_hash: str  # для простоти - звичайний рядок
    balance: float = 0.0
    is_active: bool = True

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.id == other.id