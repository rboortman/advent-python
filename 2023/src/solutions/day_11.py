from enum import Enum
from .solution import Solution


class Point(Enum):
    EMPTY = "."
    GALAXY = "#"

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.__str__()


class Space:
    def __init__(self, grid_str: str) -> None:
        self.grid = [[Point(cell) for cell in row] for row in grid_str.splitlines()]
        self.galaxies = self.find_galaxies()

    def find_galaxies(self):
        return [
            (x, y)
            for (y, row) in enumerate(self.grid)
            for (x, cell) in enumerate(row)
            if cell == Point.GALAXY
        ]

    def expand(self, size: int = 1) -> "Space":
        empty_columns = [i for i in range(len(self.grid[0]))]
        empty_rows = []

        for y, row in enumerate(self.grid):
            is_empty = True
            for x, cell in enumerate(row):
                if cell == Point.GALAXY:
                    is_empty = False
                    if x in empty_columns:
                        empty_columns.remove(x)
            if is_empty:
                empty_rows.append(y)

        for y in list(reversed(empty_rows)):
            for _ in range(size):
                self.grid.insert(y, [Point.EMPTY for _ in range(len(self.grid[y]))])

        for x in list(reversed(empty_columns)):
            for row in self.grid:
                for _ in range(size):
                    row.insert(x, Point.EMPTY)

        self.galaxies = self.find_galaxies()
        return self

    def mock_expand(self, size: int = 1) -> list[tuple[int, int]]:
        galaxy_x = [galaxy[0] for galaxy in self.galaxies]
        galaxy_y = [galaxy[1] for galaxy in self.galaxies]

        empty_columns = [i for i in range(len(self.grid[0])) if i not in galaxy_x]
        empty_rows = [i for i in range(len(self.grid)) if i not in galaxy_y]

        new_galaxies = []

        for galaxy in self.galaxies:
            x_empty = len([x for x in empty_columns if x < galaxy[0]])
            y_empty = len([y for y in empty_rows if y < galaxy[1]])

            new_galaxies.append((galaxy[0] + (x_empty * (size - 1)), galaxy[1] + (y_empty * (size - 1))))

        return new_galaxies

    def __str__(self) -> str:
        return "\n".join(["".join([str(cell) for cell in row]) for row in self.grid])

    def __repr__(self) -> str:
        return self.__str__()


class Assignment(Solution):
    def parse_input(self, input: str, is_gold: bool = False) -> Space:
        return Space(input)

    def silver(self, input: Space) -> int:
        input.expand()
        return sum(
            [
                abs(galaxy_a[0] - galaxy_b[0]) + abs(galaxy_a[1] - galaxy_b[1])
                for (i, galaxy_a) in enumerate(input.galaxies)
                for galaxy_b in input.galaxies[i + 1 :]
            ]
        )

    def gold(self, input: Space) -> int:
        mock_galaxies = input.mock_expand(1_000_000)
        return sum(
            [
                abs(galaxy_a[0] - galaxy_b[0]) + abs(galaxy_a[1] - galaxy_b[1])
                for (i, galaxy_a) in enumerate(mock_galaxies)
                for galaxy_b in mock_galaxies[i + 1 :]
            ]
        )
