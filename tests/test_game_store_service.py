import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.game import Game, GameGenre
from src.models.user import User
from src.models.purchase import Purchase
from src.repositories.game_repository import GameRepository
from src.repositories.user_repository import UserRepository
from src.repositories.purchase_repository import PurchaseRepository
from src.services.game_store_service import GameStoreService


class TestGameStoreService(unittest.TestCase):
    """Тести для бізнес-логіки магазину ігор"""

    def setUp(self):
        """Підготовка тестових даних"""
        self.game_repo = GameRepository()
        self.user_repo = UserRepository()
        self.purchase_repo = PurchaseRepository()
        self.service = GameStoreService(self.game_repo, self.user_repo, self.purchase_repo)

        # Додавання тестових ігор
        self.game1 = self.game_repo.add(Game(0, "Cyberpunk 2077", GameGenre.RPG, 299.99, "CD Projekt", 2020, True, 4.5))
        self.game2 = self.game_repo.add(Game(0, "The Witcher 3", GameGenre.RPG, 199.99, "CD Projekt", 2015, True, 4.9))
        self.game3 = self.game_repo.add(Game(0, "Stardew Valley", GameGenre.SIMULATION, 79.99, "ConcernedApe", 2016, True, 4.8))
        self.game4 = self.game_repo.add(Game(0, "CS:GO", GameGenre.ACTION, 0.0, "Valve", 2012, True, 4.2))

        # Додавання тестових користувачів
        self.user1 = self.user_repo.add(User(0, "gamer123", "gamer@test.com", "pass123", 500.0))
        self.user2 = self.user_repo.add(User(0, "noob", "noob@test.com", "pass456", 50.0))

    # ========== СЦЕНАРІЙ 1: ПОКУПКА ГРИ ==========

    def test_01_purchase_game_success(self):
        """Успішна покупка гри"""
        success, message = self.service.purchase_game(self.user1.id, self.game1.id)

        self.assertTrue(success)
        self.assertIn("Вітаємо", message)

        # Перевірка балансу
        updated_user = self.user_repo.find_by_id(self.user1.id)
        self.assertAlmostEqual(updated_user.balance, 500.0 - 299.99)

        # Перевірка створення покупки
        purchases = self.purchase_repo.find_by_user(self.user1.id)
        self.assertEqual(len(purchases), 1)
        self.assertEqual(purchases[0].game_id, self.game1.id)

    def test_02_purchase_game_insufficient_funds(self):
        """Недостатньо коштів для покупки"""
        success, message = self.service.purchase_game(self.user2.id, self.game1.id)

        self.assertFalse(success)
        self.assertIn("Недостатньо коштів", message)

    def test_03_purchase_game_already_owned(self):
        """Спроба купити гру, яка вже є в бібліотеці"""
        # Спочатку купуємо
        self.service.purchase_game(self.user1.id, self.game1.id)

        # Спроба купити знову
        success, message = self.service.purchase_game(self.user1.id, self.game1.id)

        self.assertFalse(success)
        self.assertIn("вже купили", message)

    def test_04_purchase_game_nonexistent_user(self):
        """Спроба покупки від неіснуючого користувача"""
        success, message = self.service.purchase_game(999, self.game1.id)

        self.assertFalse(success)
        self.assertIn("не знайдений", message)

    def test_05_purchase_game_nonexistent_game(self):
        """Спроба покупки неіснуючої гри"""
        success, message = self.service.purchase_game(self.user1.id, 999)

        self.assertFalse(success)
        self.assertIn("не знайдена", message)

    def test_06_purchase_unavailable_game(self):
        """Спроба покупки недоступної гри"""
        self.game_repo.delete(self.game1.id)  # Робимо гру недоступною
        success, message = self.service.purchase_game(self.user1.id, self.game1.id)

        self.assertFalse(success)
        self.assertIn("не доступна", message)

    # ========== СЦЕНАРІЙ 2: ПОВЕРНЕННЯ ГРИ ==========

    def test_07_return_game_success(self):
        """Успішне повернення гри"""
        # Спочатку купуємо
        self.service.purchase_game(self.user1.id, self.game1.id)

        # Повертаємо
        success, message = self.service.return_game(self.user1.id, self.game1.id)

        self.assertTrue(success)
        self.assertIn("повернута", message)

        # Перевірка балансу (кошти повернулись)
        updated_user = self.user_repo.find_by_id(self.user1.id)
        self.assertAlmostEqual(updated_user.balance, 500.0)

    def test_08_return_game_not_purchased(self):
        """Спроба повернути гру, яку не купували"""
        success, message = self.service.return_game(self.user1.id, self.game1.id)

        self.assertFalse(success)
        self.assertIn("не купували", message)

    def test_09_return_game_expired(self):
        """Спроба повернути гру після закінчення терміну"""
        # Модифікуємо дату покупки через рефлексію для тесту
        self.service.purchase_game(self.user1.id, self.game1.id)
        purchase = self.purchase_repo.find_user_game_purchase(self.user1.id, self.game1.id)

        # Змінюємо дату на 15 днів тому
        from datetime import datetime, timedelta
        purchase.purchase_date = datetime.now() - timedelta(days=15)
        self.purchase_repo.update(purchase)

        success, message = self.service.return_game(self.user1.id, self.game1.id)

        self.assertFalse(success)
        self.assertIn("Термін повернення минув", message)

    def test_10_return_game_wrong_user(self):
        """Спроба повернути гру іншим користувачем"""
        self.service.purchase_game(self.user1.id, self.game1.id)

        # Спроба повернути іншим користувачем
        success, message = self.service.return_game(self.user2.id, self.game1.id)

        self.assertFalse(success)
        self.assertIn("не купували", message)

    # ========== СЦЕНАРІЙ 3: ПОШУК ІГОР ==========

    def test_11_search_by_title_success(self):
        """Пошук гри за назвою (успішно)"""
        games = self.service.search_games_by_title("Witcher")
        self.assertEqual(len(games), 1)
        self.assertEqual(games[0].title, "The Witcher 3")

    def test_12_search_by_genre_success(self):
        """Пошук гри за жанром"""
        games = self.service.search_games_by_genre(GameGenre.RPG)
        self.assertEqual(len(games), 2)  # Cyberpunk і Witcher

    def test_13_search_by_price_range(self):
        """Пошук ігор в ціновому діапазоні"""
        games = self.service.search_games_by_price(50, 100)
        self.assertEqual(len(games), 1)
        self.assertEqual(games[0].title, "Stardew Valley")

    def test_14_search_not_found(self):
        """Пошук неіснуючої гри"""
        games = self.service.search_games_by_title("NonExistentGame")
        self.assertEqual(len(games), 0)

    # ========== СЦЕНАРІЙ 4: РЕЄСТРАЦІЯ КОРИСТУВАЧА ==========

    def test_15_register_user_success(self):
        """Успішна реєстрація нового користувача"""
        success, message, user = self.service.register_user("newbie", "new@test.com", "pass123")

        self.assertTrue(success)
        self.assertIn("бонус", message)
        self.assertIsNotNone(user)
        self.assertAlmostEqual(user.balance, 100.0)  # Бонус 100₴

    def test_16_register_user_duplicate_username(self):
        """Спроба реєстрації з існуючим username"""
        success, message, user = self.service.register_user("gamer123", "another@test.com", "pass")

        self.assertFalse(success)
        self.assertIn("вже існує", message)

    def test_17_register_user_duplicate_email(self):
        """Спроба реєстрації з існуючим email"""
        success, message, user = self.service.register_user("different", "gamer@test.com", "pass")

        self.assertFalse(success)
        self.assertIn("вже існує", message)

    def test_18_register_user_weak_password(self):
        """Спроба реєстрації з коротким паролем"""
        success, message, user = self.service.register_user("testuser", "test@test.com", "123")

        self.assertFalse(success)
        self.assertIn("мінімум", message)

    # ========== ДОДАТКОВІ ТЕСТИ ==========

    def test_19_add_funds_success(self):
        """Поповнення балансу"""
        success, message, balance = self.service.add_funds(self.user1.id, 100)

        self.assertTrue(success)
        self.assertAlmostEqual(balance, 600.0)

    def test_20_add_funds_negative_amount(self):
        """Поповнення на від'ємну суму"""
        success, message, balance = self.service.add_funds(self.user1.id, -50)

        self.assertFalse(success)
        self.assertIn("додатною", message)

    def test_21_get_top_games(self):
        """Отримання топ ігор за рейтингом"""
        top = self.service.get_top_games_by_rating(3)
        self.assertEqual(len(top), 3)
        self.assertEqual(top[0].title, "The Witcher 3")  # Рейтинг 4.9


if __name__ == "__main__":
    unittest.main()
