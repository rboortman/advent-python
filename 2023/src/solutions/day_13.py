import math
from enum import Enum
from .solution import Solution
import numpy as np

class Terrain(Enum):
    ROCK = "#"
    ASH = "."

    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __sub__(self, other: "Terrain") -> int:
        return 1 if self.value != other.value else 0
    
class Direction(Enum):
    VERTICAL = 1
    HORIZONTAL = 100

    def get_multiplied(self, value: int) -> int:
        return self.value * value

    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return self.__str__()
    

def is_mirrored(grid: np.ndarray) -> bool:
    return np.array_equal(grid, grid[::-1])

def is_almost_mirrored(grid: np.ndarray) -> bool:
    return sum(sum(grid - grid[::-1])) == 2
    
class Landscape:
    def __init__(self, grid_str: str, is_gold: bool = False) -> None:
        self.grid = np.array([[Terrain(cell) for cell in row] for row in grid_str.splitlines()])
        self.is_gold = is_gold

    def get_mirror_position(self) -> int:
        height, width = self.grid.shape

        for i in range(1, height - 1):
            adjusted_i = i + 1
            if is_mirrored(self.grid[:i + 1]):
                return (adjusted_i // 2) * Direction.HORIZONTAL.value
            elif is_mirrored(self.grid[i:]):
                return (adjusted_i + (height - adjusted_i) // 2) * Direction.HORIZONTAL.value
            
        transposed = self.grid.transpose()
        for i in range(1, width - 1):
            adjusted_i = i + 1
            if is_mirrored(transposed[:i + 1]):
                return (adjusted_i // 2) * Direction.VERTICAL.value
            elif is_mirrored(transposed[i:]):
                return (adjusted_i + (width - adjusted_i) // 2) * Direction.VERTICAL.value
            
    def get_almost_mirror_position(self) -> int:
        height, width = self.grid.shape

        for i in range(1, height - 1):
            adjusted_i = i + 1
            if (i+1)%2 == 0 and is_almost_mirrored(self.grid[:i + 1]):
                return (adjusted_i // 2) * Direction.HORIZONTAL.value
            elif (height-i)%2 == 0 and is_almost_mirrored(self.grid[i:]):
                return (adjusted_i + (height - adjusted_i) // 2) * Direction.HORIZONTAL.value
        
        transposed = self.grid.transpose()
        for i in range(1, width - 1):
            adjusted_i = i + 1
            if (i+1)%2 == 0 and is_almost_mirrored(transposed[:i + 1]):
                return (adjusted_i // 2) * Direction.VERTICAL.value
            elif (width-i)%2 == 0 and is_almost_mirrored(transposed[i:]):
                return (adjusted_i + (width - adjusted_i) // 2) * Direction.VERTICAL.value
            
    def __str__(self) -> str:
        return "\n".join(["".join([str(cell) for cell in row]) for row in self.grid])
    
    def __repr__(self) -> str:
        return self.__str__()


class Assignment(Solution):
    def parse_input(self, input: str, is_gold: bool = False) -> list[Landscape]:
        return [Landscape(area, is_gold=is_gold) for area in input.split("\n\n")]
    
    def silver(self, input: list[Landscape]) -> int:
        return sum([landscape.get_mirror_position() for landscape in input])
    
    def gold(self, input: list[Landscape]) -> int:
        return sum([landscape.get_almost_mirror_position() for landscape in input])