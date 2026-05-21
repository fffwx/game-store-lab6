"""DTO для користувача"""

from dataclasses import dataclass


@dataclass
class UserDTO:
    """Об'єкт передачі даних для користувача"""

    id: int
    username: str
    email: str
    balance: float

    @classmethod
    def from_user(cls, user):
        """Створює DTO з моделі User"""
        return cls(id=user.id, username=user.username, email=user.email, balance=user.balance)
