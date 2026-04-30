import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.repositories.game_repository import GameRepository
from src.repositories.user_repository import UserRepository
from src.repositories.purchase_repository import PurchaseRepository
from src.services.game_store_service import GameStoreService
from src.controllers.game_store_controller import GameStoreController
from src.models.game import Game, GameGenre


def init_test_data(game_repo, user_repo):
    """Ініціалізація тестових даних"""
    games = [
        Game(0, "Cyberpunk 2077", GameGenre.RPG, 299.99, "CD Projekt", 2020, True, 4.5),
        Game(0, "The Witcher 3", GameGenre.RPG, 199.99, "CD Projekt", 2015, True, 4.9),
        Game(0, "Stardew Valley", GameGenre.SIMULATION, 79.99, "ConcernedApe", 2016, True, 4.8),
        Game(0, "Counter-Strike 2", GameGenre.ACTION, 0.0, "Valve", 2023, True, 4.3),
        Game(0, "Baldur's Gate 3", GameGenre.RPG, 499.99, "Larian", 2023, True, 4.9),
        Game(0, "Hollow Knight", GameGenre.ACTION, 59.99, "Team Cherry", 2017, True, 4.7),
        Game(0, "Factorio", GameGenre.STRATEGY, 349.99, "Wube", 2020, True, 4.8),
    ]
    for game in games:
        game_repo.add(game)

    users = [
        User(0, "andriy_gamer", "andriy@example.com", "pass123", 1000.0),
        User(0, "oksana_player", "oksana@example.com", "pass456", 500.0),
        User(0, "dmytro_noob", "dmytro@example.com", "pass789", 150.0),
    ]
    for user in users:
        user_repo.add(user)


def print_menu():
    """Виведення меню"""
    print(" GAME STORE ")
    print("1.  Покупка гри")
    print("2.  Повернення гри")
    print("3.  Пошук ігор")
    print("4.  Реєстрація нового користувача")
    print("5.  Список всіх ігор")
    print("6.  Інформація про користувача")
    print("7.  Поповнити баланс")
    print("8.  Топ ігор за рейтингом")
    print("0.  Вихід")


def main():
    """Головна функція"""
    # Ініціалізація компонентів
    game_repo = GameRepository()
    user_repo = UserRepository()
    purchase_repo = PurchaseRepository()
    init_test_data(game_repo, user_repo)

    service = GameStoreService(game_repo, user_repo, purchase_repo)
    controller = GameStoreController(service)

    print("\n🎮 Ласкаво просимо до Game Store!")
    print("Ваш магазин цифрових ігор №1 в Україні 🇺🇦")

    while True:
        print_menu()
        choice = input("\nВиберіть опцію: ").strip()

        if choice == "1":
            # Покупка гри
            try:
                user_id = int(input("Введіть ваш ID: "))
                game_id = int(input("Введіть ID гри: "))
                result = controller.purchase_game_cli(user_id, game_id)
                print(f"\n{result}")
            except ValueError:
                print("\n❌ Помилка: введіть коректні числові значення")

        elif choice == "2":
            # Повернення гри
            try:
                user_id = int(input("Введіть ваш ID: "))
                game_id = int(input("Введіть ID гри для повернення: "))
                result = controller.return_game_cli(user_id, game_id)
                print(f"\n{result}")
            except ValueError:
                print("\n❌ Помилка: введіть коректні числові значення")

        elif choice == "3":
            # Пошук ігор
            print("\nТип пошуку:")
            print("1. За назвою")
            print("2. За жанром")
            search_type = input("Виберіть тип (1/2): ")

            if search_type == "1":
                query = input("Введіть назву гри: ")
                result = controller.search_games_cli(query, "title")
                print(result)
            elif search_type == "2":
                genres = [g.value for g in GameGenre]
                print(f"Доступні жанри: {', '.join(genres)}")
                query = input("Введіть жанр: ")
                result = controller.search_games_cli(query, "genre")
                print(result)
            else:
                print("\n❌ Невідомий тип пошуку")

        elif choice == "4":
            # Реєстрація
            username = input("Введіть username: ")
            email = input("Введіть email: ")
            password = input("Введіть пароль (мін. 4 символи): ")
            result = controller.register_user_cli(username, email, password)
            print(f"\n{result}")

        elif choice == "5":
            # Список всіх ігор
            result = controller.list_all_games_cli()
            print(result)

        elif choice == "6":
            # Інформація про користувача
            try:
                user_id = int(input("Введіть ID користувача: "))
                result = controller.user_info_cli(user_id)
                print(result)
            except ValueError:
                print("\n❌ Помилка: введіть коректний ID")

        elif choice == "7":
            # Поповнення балансу
            try:
                user_id = int(input("Введіть ваш ID: "))
                amount = float(input("Введіть суму поповнення: "))
                result = controller.add_funds_cli(user_id, amount)
                print(f"\n{result}")
            except ValueError:
                print("\n❌ Помилка: введіть коректні числові значення")

        elif choice == "8":
            # Топ ігор
            try:
                limit = int(input("Скільки ігор показати (за замовчуванням 5): ") or "5")
                result = controller.top_games_cli(limit)
                print(result)
            except ValueError:
                result = controller.top_games_cli(5)
                print(result)

        elif choice == "0":
            print("\n👋 Дякуємо за відвідування! Повертайтесь ще!")
            break

        else:
            print("\n❌ Невідома опція. Спробуйте ще раз.")


if __name__ == "__main__":
    main()