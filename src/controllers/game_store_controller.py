"""Контролер CLI - точка входу для користувача"""

from src.services.game_store_service import GameStoreService
from src.dto.game_dto import GameDTO
from src.dto.user_dto import UserDTO
from src.models.game import GameGenre


class GameStoreController:
    """Контролер для роботи з магазином ігор через CLI"""

    def __init__(self, service: GameStoreService):
        self.service = service

    def purchase_game_cli(self, user_id: int, game_id: int) -> str:
        success, message = self.service.purchase_game(user_id, game_id)
        return message

    def return_game_cli(self, user_id: int, game_id: int) -> str:
        success, message = self.service.return_game(user_id, game_id)
        return message

    def search_games_cli(self, query: str, search_type: str = "title") -> str:
        if search_type == "title":
            games = self.service.search_games_by_title(query)
        elif search_type == "genre":
            try:
                genre = GameGenre(query.lower())
                games = self.service.search_games_by_genre(genre)
            except ValueError:
                return f"Невідомий жанр: {query}"
        else:
            return "Невідомий тип пошуку"

        if not games:
            return f"Ігри за запитом '{query}' не знайдені"

        result = f"\nЗнайдено ігор: {len(games)}\n"
        result += "-" * 60 + "\n"
        for game in games:
            dto = GameDTO.from_game(game)
            result += (
                f"ID: {dto.id} | {dto.title} | {dto.genre} | "
                f"{dto.price}₴ | ⭐ {dto.rating}\n"
            )
        return result

    def register_user_cli(self, username: str, email: str, password: str) -> str:
        success, message, user = self.service.register_user(username, email, password)
        if success and user:
            dto = UserDTO.from_user(user)
            return f"{message}\nВаш ID: {dto.id} | Баланс: {dto.balance}₴"
        return message

    def list_all_games_cli(self) -> str:
        games = self.service.get_all_available_games()
        if not games:
            return "Немає доступних ігор"

        result = "\n📋 ДОСТУПНІ ІГРИ:\n" + "=" * 60 + "\n"
        for game in games:
            dto = GameDTO.from_game(game)
            result += f"🎮 ID: {dto.id} | {dto.title}\n"
            result += (
                f"   Жанр: {dto.genre} | Ціна: {dto.price}₴ | "
                f"⭐ {dto.rating}\n"
            )
            result += "-" * 50 + "\n"
        return result

    def user_info_cli(self, user_id: int) -> str:
        user = self.service.get_user_by_id(user_id)
        if not user:
            return f"Користувач з ID {user_id} не знайдений"

        dto = UserDTO.from_user(user)
        purchases = self.service.get_user_purchases(user_id)

        result = "\n👤 ІНФОРМАЦІЯ ПРО КОРИСТУВАЧА:\n"
        result += f"   ID: {dto.id}\n"
        result += f"   Ім'я: {dto.username}\n"
        result += f"   Email: {dto.email}\n"
        result += f"   Баланс: {dto.balance}₴\n"

        if purchases:
            result += f"\n📚 БІБЛІОТЕКА ІГОР ({len(purchases)}):\n"
            result += "-" * 50 + "\n"
            for purchase in purchases:
                game = self.service.get_game_by_id(purchase.game_id)
                if game:
                    result += (
                        f"   🎮 {game.title} | "
                        f"Куплено: {purchase.purchase_date.strftime('%Y-%m-%d')} | "
                        f"{purchase.price_paid}₴\n"
                    )
        else:
            result += "\n📚 Бібліотека порожня. Купіть свої перші ігри!\n"

        return result

    def add_funds_cli(self, user_id: int, amount: float) -> str:
        success, message, balance = self.service.add_funds(user_id, amount)
        if success:
            return f"{message} Поточний баланс: {balance}₴"
        return message

    def top_games_cli(self, limit: int = 5) -> str:
        games = self.service.get_top_games_by_rating(limit)
        if not games:
            return "Немає доступних ігор"

        result = f"\n🏆 ТОП-{limit} ІГОР ЗА РЕЙТИНГОМ:\n" + "=" * 50 + "\n"
        for i, game in enumerate(games, 1):
            dto = GameDTO.from_game(game)
            result += f"{i}. {dto.title} | {dto.genre} | ⭐ {dto.rating}\n"
        return result
