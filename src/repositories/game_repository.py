"""Репозиторій для роботи з іграми"""

from typing import List, Optional
from src.models.game import Game, GameGenre


class GameRepository:
    """Репозиторій для управління даними ігор"""

    def __init__(self):
        self._games: dict[int, Game] = {}
        self._next_id = 1

    def add(self, game: Game) -> Game:
        """Додає нову гру"""
        if game.id == 0:
            game.id = self._next_id
            self._next_id += 1
        self._games[game.id] = game
        return game

    def find_by_id(self, game_id: int) -> Optional[Game]:
        """Знаходить гру за ID"""
        return self._games.get(game_id)

    def find_by_title(self, title: str) -> List[Game]:
        """Знаходить ігри за назвою (частковий збіг)"""
        title_lower = title.lower()
        return [
            game for game in self._games.values()
            if title_lower in game.title.lower() and game.is_available
        ]

    def find_by_genre(self, genre: GameGenre) -> List[Game]:
        """Знаходить ігри за жанром"""
        return [
            game for game in self._games.values()
            if game.genre == genre and game.is_available
        ]

    def find_by_price_range(self, min_price: float, max_price: float) -> List[Game]:
        """Знаходить ігри в ціновому діапазоні"""
        return [
            game for game in self._games.values()
            if min_price <= game.price <= max_price and game.is_available
        ]

    def find_all_available(self) -> List[Game]:
        """Повертає всі доступні ігри"""
        return [game for game in self._games.values() if game.is_available]

    def find_all(self) -> List[Game]:
        """Повертає всі ігри (включаючи видалені)"""
        return list(self._games.values())

    def update(self, game: Game) -> Game:
        """Оновлює інформацію про гру"""
        if game.id in self._games:
            self._games[game.id] = game
        return game

    def delete(self, game_id: int) -> bool:
        """М'яке видалення гри (робимо недоступною)"""
        game = self._games.get(game_id)
        if game:
            game.is_available = False
            return True
        return False

    def clear(self):
        """Очищує репозиторій (для тестів)"""
        self._games.clear()
        self._next_id = 1
