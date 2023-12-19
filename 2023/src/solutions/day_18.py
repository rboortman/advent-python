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
            "0": Instruction.EAST,
            "D": Instruction.SOUTH,
            "1": Instruction.SOUTH,
            "L": Instruction.WEST,
            "2": Instruction.WEST,
            "U": Instruction.NORTH,
            "3": Instruction.NORTH,
        }[input]


class Grid:
    def __init__(self, input: str, is_gold: bool = False) -> None:
        self.instructions = [
            (
                Instruction.parse(line.split(" ")[0]),
                int(line.split(" ")[1]),
                line.split(" ")[2][2:-1],
            )
            for line in input.splitlines()
        ]
        if is_gold:
            self.instructions = [
                (
                    Instruction.parse(instruction[2][-1]),
                    int(instruction[2][:-1], 16),
                    instruction[2],
                )
                for instruction in self.instructions
            ]

        x_min_max = functools.reduce(
            lambda acc, ins: (
                min(
                    acc[0],
                    acc[2] + ins[1] if ins[0] == Instruction.EAST else acc[2] - ins[1],
                ),
                max(
                    acc[1],
                    acc[2] + ins[1] if ins[0] == Instruction.EAST else acc[2] - ins[1],
                ),
                acc[2] + ins[1] if ins[0] == Instruction.EAST else acc[2] - ins[1],
            ),
            [
                instruction
                for instruction in self.instructions
                if instruction[0] in [Instruction.EAST, Instruction.WEST]
            ],
            (0, 0, 0),
        )
        y_min_max = functools.reduce(
            lambda acc, ins: (
                min(
                    acc[0],
                    acc[2] + ins[1] if ins[0] == Instruction.SOUTH else acc[2] - ins[1],
                ),
                max(
                    acc[1],
                    acc[2] + ins[1] if ins[0] == Instruction.SOUTH else acc[2] - ins[1],
                ),
                acc[2] + ins[1] if ins[0] == Instruction.SOUTH else acc[2] - ins[1],
            ),
            [
                instruction
                for instruction in self.instructions
                if instruction[0] in [Instruction.NORTH, Instruction.SOUTH]
            ],
            (0, 0, 0),
        )
        self.width = abs(x_min_max[0]) + abs(x_min_max[1])
        self.height = abs(y_min_max[0]) + abs(y_min_max[1])
        self.start = (abs(x_min_max[0]), abs(y_min_max[0]))

    def calculate_area(self) -> int:
        area = 0
        y = self.start[1]
        for i, instruction in enumerate(self.instructions):
            if instruction[0] == Instruction.NORTH:
                y -= instruction[1]
            elif instruction[0] == Instruction.SOUTH:
                y += instruction[1]
            elif instruction[0] == Instruction.EAST:
                width = instruction[1]
                if self.instructions[i + 1][0] != self.instructions[i - 1][0]:
                    if self.instructions[i + 1][0] == Instruction.NORTH:
                        width -= 1
                    else:
                        width += 1
                area -= width * y
            elif instruction[0] == Instruction.WEST:
                width = instruction[1]
                if self.instructions[i + 1][0] != self.instructions[i - 1][0]:
                    if self.instructions[i + 1][0] == Instruction.NORTH:
                        width += 1
                    else:
                        width -= 1
                area += width * (y + 1)
        return area

    def __str__(self) -> str:
        return "\n".join([str(instruction) for instruction in self.instructions])

    def __repr__(self) -> str:
        return self.__str__()


class Assignment(Solution):
    def parse_input(self, input: str, is_gold: bool = False) -> Grid:
        return Grid(input, is_gold=is_gold)

    def silver(self, input: Grid) -> int:
        return input.calculate_area()

    def gold(self, input: Grid) -> int:
        return input.calculate_area()
