"""Сервісний шар з бізнес-логікою магазину ігор"""

from typing import List, Tuple, Optional
from datetime import datetime

from src.models.game import Game, GameGenre
from src.models.user import User
from src.models.purchase import Purchase
from src.repositories.game_repository import GameRepository
from src.repositories.user_repository import UserRepository
from src.repositories.purchase_repository import PurchaseRepository


class GameStoreService:
    """Сервіс для роботи з магазином ігор"""

    RETURN_DAYS_LIMIT = 14
    REGISTRATION_BONUS = 100.0

    def __init__(self, game_repo: GameRepository, user_repo: UserRepository, purchase_repo: PurchaseRepository):
        self.game_repo = game_repo
        self.user_repo = user_repo
        self.purchase_repo = purchase_repo

    def purchase_game(self, user_id: int, game_id: int) -> Tuple[bool, str]:
        """Купівля гри користувачем"""
        user = self.user_repo.find_by_id(user_id)
        if not user:
            return False, f"Користувач з ID {user_id} не знайдений"

        if not user.is_active:
            return False, "Ваш акаунт деактивовано. Зверніться до підтримки"

        game = self.game_repo.find_by_id(game_id)
        if not game:
            return False, f"Гра з ID {game_id} не знайдена"

        if not game.is_available:
            return False, f"Гра '{game.title}' більше не доступна для покупки"

        existing_purchase = self.purchase_repo.find_user_game_purchase(user_id, game_id)
        if existing_purchase:
            return False, f"Ви вже купили гру '{game.title}'"

        if user.balance < game.price:
            return False, (f"Недостатньо коштів. " f"Потрібно: {game.price}₴, доступно: {user.balance}₴")

        user.balance -= game.price
        self.user_repo.update(user)

        purchase = Purchase(id=0, user_id=user_id, game_id=game_id, purchase_date=datetime.now(), price_paid=game.price)
        self.purchase_repo.add(purchase)

        return True, f"Вітаємо! Ви купили гру '{game.title}' за {game.price}₴"

    def return_game(self, user_id: int, game_id: int) -> Tuple[bool, str]:
        """Повернення гри користувачем (протягом 14 днів)"""
        user = self.user_repo.find_by_id(user_id)
        if not user:
            return False, f"Користувач з ID {user_id} не знайдений"

        game = self.game_repo.find_by_id(game_id)
        if not game:
            return False, f"Гра з ID {game_id} не знайдена"

        purchase = self.purchase_repo.find_user_game_purchase(user_id, game_id)
        if not purchase:
            return False, f"Ви не купували гру '{game.title}'"

        days_since = purchase.days_since_purchase()
        if days_since > self.RETURN_DAYS_LIMIT:
            return False, (
                f"Термін повернення минув. Ви купили гру {days_since} днів тому "
                f"(ліміт: {self.RETURN_DAYS_LIMIT} днів)"
            )

        user.balance += purchase.price_paid
        self.user_repo.update(user)

        purchase.is_returned = True
        purchase.return_date = datetime.now()
        self.purchase_repo.update(purchase)

        return True, f"Гра '{game.title}' повернута. Вам повернуто {purchase.price_paid}₴"

    def search_games_by_title(self, title: str) -> List[Game]:
        """Пошук ігор за назвою"""
        return self.game_repo.find_by_title(title)

    def search_games_by_genre(self, genre: GameGenre) -> List[Game]:
        """Пошук ігор за жанром"""
        return self.game_repo.find_by_genre(genre)

    def search_games_by_price(self, min_price: float, max_price: float) -> List[Game]:
        """Пошук ігор в ціновому діапазоні"""
        return self.game_repo.find_by_price_range(min_price, max_price)

    def get_game_by_id(self, game_id: int) -> Optional[Game]:
        """Отримання гри за ID"""
        return self.game_repo.find_by_id(game_id)

    def get_all_available_games(self) -> List[Game]:
        """Отримання всіх доступних ігор"""
        return self.game_repo.find_all_available()

    def register_user(self, username: str, email: str, password: str) -> Tuple[bool, str, Optional[User]]:
        """Реєстрація нового користувача"""
        if self.user_repo.username_exists(username):
            return False, f"Користувач з іменем '{username}' вже існує", None

        if self.user_repo.email_exists(email):
            return False, f"Користувач з email '{email}' вже існує", None

        if not password or len(password) < 4:
            return False, "Пароль повинен містити мінімум 4 символи", None

        user = User(id=0, username=username, email=email, password_hash=password, balance=self.REGISTRATION_BONUS)
        created_user = self.user_repo.add(user)

        return True, (f"Вітаємо, {username}! " f"Ви отримали бонус {self.REGISTRATION_BONUS}₴ на рахунок"), created_user

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Отримання користувача за ID"""
        return self.user_repo.find_by_id(user_id)

    def get_user_purchases(self, user_id: int) -> List[Purchase]:
        """Отримання всіх покупок користувача"""
        return self.purchase_repo.find_by_user(user_id)

    def add_funds(self, user_id: int, amount: float) -> Tuple[bool, str, float]:
        """Поповнення балансу користувача"""
        if amount <= 0:
            return False, "Сума поповнення має бути додатною", 0

        user = self.user_repo.find_by_id(user_id)
        if not user:
            return False, f"Користувач з ID {user_id} не знайдений", 0

        user.balance += amount
        self.user_repo.update(user)

        return True, f"Рахунок поповнено на {amount}₴", user.balance

    def get_top_games_by_rating(self, limit: int = 5) -> List[Game]:
        """Отримання топ ігор за рейтингом"""
        games = self.game_repo.find_all_available()
        games.sort(key=lambda g: g.rating, reverse=True)
        return games[:limit]
