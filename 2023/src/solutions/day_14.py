from enum import Enum
from tqdm import tqdm
from .solution import Solution


class Direction(Enum):
    NORTH = (0, -1)
    EAST = (1, 0)
    SOUTH = (0, 1)
    WEST = (-1, 0)


class Rock(Enum):
    ROUND = "O"
    SQUARE = "#"
    EMPTY = "."

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value


class Platform:
    def __init__(self, input: str):
        self.grid = [[Rock(char) for char in line] for line in input.split("\n")]

    def move_rock(self, position: tuple[int, int], direction: Direction):
        x, y = position
        self.grid[y][x] = Rock.EMPTY
        dx, dy = direction.value
        while (
            0 <= x + dx < len(self.grid[0])
            and 0 <= y + dy < len(self.grid)
            and self.grid[y + dy][x + dx] == Rock.EMPTY
        ):
            x += dx
            y += dy
        self.grid[y][x] = Rock.ROUND

    def move_rocks(self, direction: Direction) -> "Platform":
        y_step, y_start, y_end = (
            (1, 0, len(self.grid))
            if direction != Direction.SOUTH
            else (-1, len(self.grid) - 1, -1)
        )
        for y in range(y_start, y_end, y_step):
            x_step, x_start, x_end = (
                (1, 0, len(self.grid[y]))
                if direction != Direction.EAST
                else (-1, len(self.grid[y]) - 1, -1)
            )
            for x in range(x_start, x_end, x_step):
                if self.grid[y][x] == Rock.ROUND:
                    self.move_rock((x, y), direction=direction)
        return self

    def count_rocks(self) -> int:
        return sum(
            [
                i + 1
                for (i, row) in enumerate(reversed(self.grid))
                for rock in row
                if rock == Rock.ROUND
            ]
        )

    def spin(self) -> "Platform":
        self.move_rocks(Direction.NORTH)
        self.move_rocks(Direction.WEST)
        self.move_rocks(Direction.SOUTH)
        self.move_rocks(Direction.EAST)
        return self

    def __str__(self):
        return "\n".join(["".join([str(rock) for rock in row]) for row in self.grid])

    def __repr__(self):
        return str(self)

class Memoize:
    def __init__(self, f):
        self.f = f
        self.memo = {}
    def __call__(self, *args):
        if not args in self.memo:
            self.memo[args] = self.f(*args)
        return self.memo[args]

@Memoize
def spin(platform: str) -> str:
    p = Platform(platform)
    return str(p.spin())


class Assignment(Solution):
    def parse_input(self, input: str, is_gold: bool = False) -> Platform:
        return Platform(input)

    def silver(self, input: Platform) -> int:
        return input.move_rocks(Direction.NORTH).count_rocks()

    def gold(self, input: Platform) -> int:
        try_value = 1_000_000_000
        input_str = str(input)
        # for _ in tqdm(range(try_value)):
        for _ in range(try_value):
            input_str = spin(input_str)

        return Platform(input_str).count_rocks()
