from typing import List, Optional
from src.models.user import User


class UserRepository:
    """Репозиторій для управління даними користувачів"""

    def __init__(self):
        self._users: dict[int, User] = {}
        self._usernames: set[str] = set()
        self._emails: set[str] = set()
        self._next_id = 1

    def add(self, user: User) -> User:
        """Додає нового користувача"""
        if user.id == 0:
            user.id = self._next_id
            self._next_id += 1
        self._users[user.id] = user
        self._usernames.add(user.username)
        self._emails.add(user.email)
        return user

    def find_by_id(self, user_id: int) -> Optional[User]:
        """Знаходить користувача за ID"""
        return self._users.get(user_id)

    def find_by_username(self, username: str) -> Optional[User]:
        """Знаходить користувача за username"""
        for user in self._users.values():
            if user.username == username:
                return user
        return None

    def find_by_email(self, email: str) -> Optional[User]:
        """Знаходить користувача за email"""
        for user in self._users.values():
            if user.email == email:
                return user
        return None

    def find_all(self) -> List[User]:
        """Повертає всіх користувачів"""
        return [user for user in self._users.values() if user.is_active]

    def update(self, user: User) -> User:
        """Оновлює інформацію про користувача"""
        if user.id in self._users:
            self._users[user.id] = user
        return user

    def username_exists(self, username: str) -> bool:
        """Перевіряє, чи існує username"""
        return username in self._usernames

    def email_exists(self, email: str) -> bool:
        """Перевіряє, чи існує email"""
        return email in self._emails

    def clear(self):
        """Очищує репозиторій (для тестів)"""
        self._users.clear()
        self._usernames.clear()
        self._emails.clear()
        self._next_id = 1