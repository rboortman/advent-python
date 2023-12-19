import functools
from enum import Enum
from .solution import Solution


class Terrain(Enum):
    EMPTY = "."
    HOLE = "#"
    FILLED = "O"

    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return self.__str__()

class Instruction(Enum):
    NORTH = (0, -1)
    EAST = (1, 0)
    SOUTH = (0, 1)
    WEST = (-1, 0)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.__str__()

    @staticmethod
    def parse(input: str) -> "Instruction":
        return {
            "R": Instruction.EAST,
            "D": Instruction.SOUTH,
            "L": Instruction.WEST,
            "U": Instruction.NORTH,
        }[input]


class Grid:
    def __init__(self, input: str) -> None:
        self.instructions = [
            (
                Instruction.parse(line.split(" ")[0]),
                int(line.split(" ")[1]),
                line.split(" ")[2][2:-1],
            )
            for line in input.splitlines()
        ]
        self.width = functools.reduce(
            lambda acc, ins: (
                max(
                    acc[0],
                    acc[1] + ins[1] if ins[0] == Instruction.EAST else acc[1] - ins[1],
                ),
                acc[1] + ins[1] if ins[0] == Instruction.EAST else acc[1] - ins[1],
            ),
            [
                instruction
                for instruction in self.instructions
                if instruction[0] in [Instruction.EAST, Instruction.WEST]
            ],
            (0, 0),
        )[0]
        self.height = functools.reduce(
            lambda acc, ins: (
                max(
                    acc[0],
                    acc[1] + ins[1] if ins[0] == Instruction.SOUTH else acc[1] - ins[1],
                ),
                acc[1] + ins[1] if ins[0] == Instruction.SOUTH else acc[1] - ins[1],
            ),
            [
                instruction
                for instruction in self.instructions
                if instruction[0] in [Instruction.NORTH, Instruction.SOUTH]
            ],
            (0, 0),
        )[0]
        self.grid = [[Terrain.EMPTY for _ in range(self.width + 1)] for _ in range(self.height + 1)]

        pointer = (0, 0)
        for instruction in self.instructions:
            for _ in range(instruction[1]):
                pointer = (
                    pointer[0] + instruction[0].value[0],
                    pointer[1] + instruction[0].value[1],
                )
                self.grid[pointer[1]][pointer[0]] = Terrain.HOLE

    def count_hole_sections(
        self, coord: tuple[int, int]
    ) -> int:
        x, y = coord
        tile = self.grid[y][x]
        count = 0
        last_direction = None

        for i, tile in enumerate(self.grid[y][x:]):
            if tile == Terrain or checked_grid[y][x + i] != Checked.LOOP:
                last_direction = None
            elif tile == Section.NORTH_SOUTH:
                last_direction = None
                count += 1
            else:
                if tile.has_east():
                    if tile.has_north():
                        last_direction = Direction.NORTH
                    elif tile.has_south():
                        last_direction = Direction.SOUTH
                else:
                    if (tile.has_north() and last_direction == Direction.SOUTH) or (
                        tile.has_south() and last_direction == Direction.NORTH
                    ):
                        count += 1
                    last_direction = None

        return count

    def fill(self, pointer: tuple[int, int], direction: Instruction) -> None:
        for (y, row) in enumerate(self.grid):
            for (x, tile) in enumerate(row):
                if tile == Terrain.HOLE:
                    continue
                edges = []

        if self.grid[pointer[1]][pointer[0]] == Terrain.HOLE:
            return
        while self.grid[pointer[1]][pointer[0]] == Terrain.EMPTY:
            self.grid[pointer[1]][pointer[0]] = Terrain.HOLE
            pointer = (
                pointer[0] + direction.value[0],
                pointer[1] + direction.value[1],
            )

    def __str__(self) -> str:
        return "\n".join(["".join([str(char) for char in line]) for line in self.grid])
    
    def __repr__(self) -> str:
        return self.__str__()


class Assignment(Solution):
    def parse_input(self, input: str, is_gold: bool = False) -> Grid:
        return Grid(input)

    def silver(self, input: Grid) -> int:
        print(input)
        return 0

    def gold(self, input: Grid) -> int:
        return 0
