from enum import Enum
from .solution import Solution


class Checked(Enum):
    NOT_CHECKED = 0
    LOOP = 1
    OUTSIDE_LOOP = 2
    INSIDE_LOOP = 3


class Direction(Enum):
    NORTH = (0, -1)
    EAST = (1, 0)
    SOUTH = (0, 1)
    WEST = (-1, 0)


class Section(Enum):
    NORTH_SOUTH = "|"
    EAST_WEST = "-"
    NORTH_EAST = "L"
    NORTH_WEST = "J"
    SOUTH_EAST = "F"
    SOUTH_WEST = "7"
    GROUND = "."
    START = "S"

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.__str__()

    def has_north(self) -> bool:
        return self in [Section.NORTH_SOUTH, Section.NORTH_EAST, Section.NORTH_WEST]

    def has_south(self) -> bool:
        return self in [Section.NORTH_SOUTH, Section.SOUTH_EAST, Section.SOUTH_WEST]

    def has_east(self) -> bool:
        return self in [Section.EAST_WEST, Section.NORTH_EAST, Section.SOUTH_EAST]

    def has_west(self) -> bool:
        return self in [Section.EAST_WEST, Section.NORTH_WEST, Section.SOUTH_WEST]


class Pipes:
    def __init__(self, grid_str: str) -> None:
        self.grid = [[Section(cell) for cell in row] for row in grid_str.splitlines()]
        self.start = self.find_start()

        start_x, start_y = self.start

        if start_y > 0 and self.grid[start_y - 1][start_x].has_south():
            if start_y < len(self.grid) and self.grid[start_y + 1][start_x].has_north():
                self.grid[start_y][start_x] = Section.NORTH_SOUTH
            elif start_x > 0 and self.grid[start_y][start_x - 1].has_east():
                self.grid[start_y][start_x] = Section.NORTH_EAST
            elif (
                start_x < len(self.grid[start_y - 1])
                and self.grid[start_y][start_x + 1].has_west()
            ):
                self.grid[start_y][start_x] = Section.NORTH_WEST
        elif start_y < len(self.grid) and self.grid[start_y + 1][start_x].has_north():
            if start_x > 0 and self.grid[start_y][start_x - 1].has_east():
                self.grid[start_y][start_x] = Section.SOUTH_WEST
            elif (
                start_x < len(self.grid[start_y - 1])
                and self.grid[start_y][start_x + 1].has_west()
            ):
                self.grid[start_y][start_x] = Section.SOUTH_EAST
        elif self.grid[start_y][start_x - 1].has_east():
            self.grid[start_y][start_x] = Section.EAST_WEST

    def find_start(self) -> tuple[int, int]:
        for y, row in enumerate(self.grid):
            for x, section in enumerate(row):
                if section == Section.START:
                    return (x, y)
        raise ValueError("No start found")

    def get_loop_coordinates(self) -> list[tuple[int, int]]:
        x, y = self.start
        section = self.grid[y][x]
        coords = [self.start]

        if section.has_north():
            direction = Direction.NORTH
        elif section.has_south():
            direction = Direction.SOUTH
        elif section.has_east():
            direction = Direction.EAST
        elif section.has_west():
            direction = Direction.WEST

        while x != self.start[0] or y != self.start[1] or len(coords) <= 1:
            if direction == Direction.NORTH:
                if section.has_east():
                    direction = Direction.EAST
                elif section.has_west():
                    direction = Direction.WEST
                elif section.has_north():
                    direction = Direction.NORTH
            elif direction == Direction.SOUTH:
                if section.has_east():
                    direction = Direction.EAST
                elif section.has_west():
                    direction = Direction.WEST
                elif section.has_south():
                    direction = Direction.SOUTH
            elif direction == Direction.EAST:
                if section.has_south():
                    direction = Direction.SOUTH
                elif section.has_north():
                    direction = Direction.NORTH
                elif section.has_east():
                    direction = Direction.EAST
            elif direction == Direction.WEST:
                if section.has_south():
                    direction = Direction.SOUTH
                elif section.has_north():
                    direction = Direction.NORTH
                elif section.has_west():
                    direction = Direction.WEST

            x += direction.value[0]
            y += direction.value[1]
            section = self.grid[y][x]
            coords.append((x, y))

        return coords

    def count_loop_sections(
        self, coord: tuple[int, int], checked_grid: list[list[Checked]]
    ) -> int:
        x, y = coord
        section = self.grid[y][x]
        count = 0
        last_direction = None

        for i, section in enumerate(self.grid[y][x:]):
            if section == Section.GROUND or checked_grid[y][x + i] != Checked.LOOP:
                last_direction = None
            elif section == Section.NORTH_SOUTH:
                last_direction = None
                count += 1
            else:
                if section.has_east():
                    if section.has_north():
                        last_direction = Direction.NORTH
                    elif section.has_south():
                        last_direction = Direction.SOUTH
                else:
                    if (section.has_north() and last_direction == Direction.SOUTH) or (
                        section.has_south() and last_direction == Direction.NORTH
                    ):
                        count += 1
                    last_direction = None

        return count

    def count_inside_loop(self) -> list[tuple[int, int]]:
        checked_grid = [[Checked.NOT_CHECKED for _ in row] for row in self.grid]
        loop = self.get_loop_coordinates()
        for x, y in loop:
            checked_grid[y][x] = Checked.LOOP

        for y, row in enumerate(checked_grid):
            for x, section in enumerate(row):
                if section == Checked.LOOP:
                    continue

                if 0 < x < len(row) - 1 and 0 < y < len(self.grid) - 1:
                    if self.count_loop_sections((x, y), checked_grid) % 2 == 0:
                        checked_grid[y][x] = Checked.OUTSIDE_LOOP
                    else:
                        checked_grid[y][x] = Checked.INSIDE_LOOP
                else:
                    checked_grid[y][x] = Checked.OUTSIDE_LOOP

        return sum(
            [
                sum([1 for section in row if section == Checked.INSIDE_LOOP])
                for row in checked_grid
            ]
        )

    def __getitem__(self, index: tuple[int, int]) -> Section:
        return self.grid[index[1]][index[0]]

    def __str__(self) -> str:
        return (
            "\n".join(["".join([str(cell) for cell in row]) for row in self.grid])
            + f"\nStarting position: {self.start}"
        )

    def __repr__(self) -> str:
        return self.__str__()


class Assignment(Solution):
    def parse_input(self, input: str, is_gold: bool = False) -> Pipes:
        return Pipes(input)

    def silver(self, input: Pipes) -> int:
        return int(len(input.get_loop_coordinates()) / 2)

    def gold(self, input: Pipes) -> int:
        return input.count_inside_loop()
