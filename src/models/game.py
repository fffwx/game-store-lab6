"""Модель гри"""

from dataclasses import dataclass
from enum import Enum


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
    is_available: bool = True
    rating: float = 0.0

    def __eq__(self, other):
        if not isinstance(other, Game):
            return False
        return self.id == other.id
