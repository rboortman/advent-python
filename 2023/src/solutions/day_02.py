from enum import Enum
from .solution import Solution

class Color(Enum):
    Blue = "blue"
    Green = "green"
    Red = "red"

class Cubes:
    def __init__(self, color: Color, value: int) -> None:
        self.color = color
        self.value = value
    
    def __repr__(self) -> str:
        return f"({self.color}: {self.value})"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Cubes):
            return NotImplemented
        return self.color == other.color and self.value == other.value
    
    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)
    
    def __le__(self, other: object) -> bool:
        if not isinstance(other, Cubes) or self.color != other.color:
            return NotImplemented
        return self.value <= other.value
    
    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Cubes) or self.color != other.color:
            return NotImplemented
        return self.value < other.value
    
    def __ge__(self, other: object) -> bool:
        if not isinstance(other, Cubes) or self.color != other.color:
            return NotImplemented
        return self.value >= other.value
    
    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Cubes) or self.color != other.color:
            return NotImplemented
        return self.value > other.value

class Assignment(Solution):
    def parse_input(self, input: str, is_gold: bool = False) -> list[dict["id": int, "red": list[Cubes], "green": list[Cubes], "blue": list[Cubes]]]:
        games = []
        lines = input.splitlines()
        for line in lines:
            [game, all_draws] = line.split(": ")
            [_game_name, game_id] = game.split(" ")
            game_id = int(game_id)
            game_dict = {
                "id": game_id,
                "red": [],
                "green": [],
                "blue": [],
            }
            
            draws = all_draws.split("; ")
            for draw in draws:
                cubes_string = draw.split(", ")
                cubes = {
                    Color.Blue: 0,
                    Color.Green: 0,
                    Color.Red: 0
                }
                for cube_string in cubes_string:
                    [value, color] = cube_string.split(" ")
                    cubes[Color(color)] = int(value)
                    
                for color, value in cubes.items():
                    game_dict[color.name.lower()].append(Cubes(color, value))
                
            games.append(game_dict)
          
                
        return games
    
    def silver(self, input: list[dict["id": int, "red": list[Cubes], "green": list[Cubes], "blue": list[Cubes]]]) -> int:
        filtered_games = filter(lambda game: max(game["red"]).value <= 12 and max(game["green"]).value <= 13 and max(game["blue"]).value <= 14, input)
        return sum(map(lambda game: game["id"], filtered_games))
    
    def gold(self, input: list[dict["id": int, "red": list[Cubes], "green": list[Cubes], "blue": list[Cubes]]]) -> int:
        return sum(map(lambda game: max(game["red"]).value * max(game["blue"]).value * max(game["green"]).value, input))