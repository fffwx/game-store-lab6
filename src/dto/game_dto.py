from dataclasses import dataclass


@dataclass
class GameDTO:
    """Об'єкт передачі даних для гри"""
    id: int
    title: str
    genre: str
    price: float
    developer: str
    release_year: int
    rating: float

    @classmethod
    def from_game(cls, game):
        """Створює DTO з моделі Game"""
        return cls(
            id=game.id,
            title=game.title,
            genre=game.genre.value,
            price=game.price,
            developer=game.developer,
            release_year=game.release_year,
            rating=game.rating
        )