import math
from typing import Union
from enum import Enum
from .solution import Solution

class CellType(Enum):
    Empty = "."
    Number = "#"
    Symbol = "X"
    
class Cell:
    def __init__(self, value: Union[int, str], type: CellType) -> None:
        self.value = value
        self.type = type
    
    def __repr__(self) -> str:
        return f"({self.value}, {self.type.name})"


class Grid:
    def __init__(self, width: int, height: int, default: Cell = Cell(" ", CellType.Empty)) -> None:
        self.width = width
        self.height = height
        self.default = default
        self.grid = [[self.default for _ in range(self.width)] for _ in range(self.height)]
        self.part_numbers = []
        self.symbols = []
    
    def __repr__(self) -> str:
        index = [["     "],["     "],["     "]]
        for i in range(self.width):
            i_padded = str(i).rjust(3)
            index[0].append(i_padded[0])
            index[1].append(i_padded[1])
            index[2].append(i_padded[2])
        
        top_bottom = "    +" + "-" * self.width + "+\n"
        grid = "".join(index[0]) + "\n" + "".join(index[1]) + "\n" + "".join(index[2]) + "\n" + top_bottom + "\n".join([str(index).rjust(3) + " |" + "".join([str(cell.value) for cell in row]) + "| " + str(index).ljust(3) for (index, row) in enumerate(self.grid)]) + "\n" + top_bottom + "".join(index[2]) + "\n" + "".join(index[1]) + "\n" + "".join(index[0]) + "\n"
        
        # return grid
        return grid + "\nPart numbers:\n" + "\n".join([f"{i}: {part_number}" for i, part_number in enumerate(self.part_numbers)]) + "\n\nSymbols:\n" + "\n".join([f"{i}: {symbol}" for i, symbol in enumerate(self.symbols)]) + "\n"
    
    def __getitem__(self, key: tuple[int, int]) -> Cell:
        return self.grid[key[1]][key[0]]
    
    def __setitem__(self, key: tuple[int, int], value: Cell) -> None:
        self.grid[key[1]][key[0]] = value

    def parse_input(input: str) -> "Grid":
        lines = input.splitlines()
        width = len(lines[0])
        height = len(lines)
        grid = Grid(width, height)
        part_numbers = []
        is_part_number = False
        begin = None
        end = None
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == CellType.Empty.value:
                    if is_part_number:
                        part_numbers.append((begin, end))
                        is_part_number = False
                        begin = None
                        end = None
                    continue
                
                elif char.isdigit():
                    grid[x, y] = Cell(int(char), CellType.Number)
                    if not is_part_number:
                        is_part_number = True
                        begin = (x, y)
                    end = (x, y)

                else:
                    grid[x, y] = Cell(char, CellType.Symbol)
                    grid.symbols.append((x, y))
                    if is_part_number:
                        part_numbers.append((begin, end))
                        is_part_number = False
                        begin = None
                        end = None

            if is_part_number:
                part_numbers.append((begin, end))
                is_part_number = False
                begin = None
                end = None

        grid.part_numbers = part_numbers
        return grid
    
    def is_coord_within_square(self, coord: tuple[int, int], square: tuple[tuple[int, int], tuple[int, int]]) -> bool:
        square_adjusted = ((max(square[0][0], 0), max(square[0][1], 0)), (min(square[1][0], self.width - 1), min(square[1][1], self.height - 1)))
        return square_adjusted[0][0] <= coord[0] <= square_adjusted[1][0] and square_adjusted[0][1] <= coord[1] <= square_adjusted[1][1]
    
    def get_part_number(self, index: int) -> int:
        part_coords = self.part_numbers[index]
        part_number = self.grid[part_coords[0][1]][part_coords[0][0]:part_coords[1][0] + 1]
        return int("".join(map(lambda cell: str(cell.value), part_number)))

    def has_symbol_next_to_part(self, index: int) -> bool:
        part_coords = self.part_numbers[index]
        for symbol in self.symbols:
            if self.is_coord_within_square(symbol, ((part_coords[0][0] - 1, part_coords[0][1] - 1), (part_coords[1][0] + 1, part_coords[1][1] + 1))):
                return True
        return False
    
    def get_all_star_symbols(self) -> list[int]:
        return list(filter(lambda i: self.grid[self.symbols[i][1]][self.symbols[i][0]].value == "*", range(len(self.symbols))))
    
    def get_adjacent_parts(self, coord: tuple[int, int]) -> list[int]:
        adjacent_parts = []
        for (index, part_coords) in enumerate(self.part_numbers):
            if self.is_coord_within_square(coord, ((part_coords[0][0] - 1, part_coords[0][1] - 1), (part_coords[1][0] + 1, part_coords[1][1] + 1))):
                adjacent_parts.append(index)
        return adjacent_parts

class Assignment(Solution):
    def parse_input(self, input: str, is_gold: bool = False) -> Grid:
        return Grid.parse_input(input)
    
    def silver(self, input: Grid) -> int:
        return sum([input.get_part_number(i) for i in range(len(input.part_numbers)) if input.has_symbol_next_to_part(i)])
    
    def gold(self, input: Grid) -> int:
        symbols = input.get_all_star_symbols()
        return sum(map(math.prod, map(lambda parts: map(input.get_part_number, parts), filter(lambda parts: len(parts) > 1, [input.get_adjacent_parts(input.symbols[symbol]) for symbol in symbols]))))