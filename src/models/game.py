from dataclasses import dataclass
from enum import Enum
from typing import Optional


class GameGenre(Enum):
    """Жанри ігор"""
    ACTION = "action"
    RPG = "rpg"
    STRATEGY = "strategy"
    SIMULATION = "simulation"
    SPORTS = "sports"
    PUZZLE = "puzzle"
    INDIE = "indie"


@dataclass
class Game:
    """Модель гри"""
    id: int
    title: str
    genre: GameGenre
    price: float
    developer: str
    release_year: int
    is_available: bool = True  # True - гра доступна для покупки
    rating: float = 0.0

    def __eq__(self, other):
        if not isinstance(other, Game):
            return False
        return self.id == other.id