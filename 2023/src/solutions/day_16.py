from enum import Enum
from .solution import Solution

class Direction(Enum):
    NORTH = (0, -1)
    EAST = (1, 0)
    SOUTH = (0, 1)
    WEST = (-1, 0)

    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return self.__str__()

class Tile(Enum):
    SPLITTER_VERTICAL = "|"
    SPLITTER_HORIZONTAL = "-"
    MIRROR_FORWARD = "/"
    MIRROR_BACKWARD = "\\"
    EMPTY = "."

    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return self.__str__()

class Memoize:
    def __init__(self, f):
        self.f = f
        self.memo = {}
    def __call__(self, *args):
        if not args in self.memo:
            self.memo[args] = self.f(*args)
        # print(f"Memoized: {args}")
        return self.memo[args]

class Grid:
    def __init__(self, input: str):
        self.grid = [[Tile(char) for char in line] for line in input.split("\n")]
        self.width = len(self.grid[0])
        self.height = len(self.grid)
        self.passed_through = dict()

    def get_next_tile(self, coord: tuple[int, int], direction: Direction) -> (Tile, tuple[int, int], set[tuple[int, int]]):
        x, y = coord
        tile = None
        passed_through = set()
        while tile is None:
            x += direction.value[0]
            y += direction.value[1]
            if x < 0 or x >= self.width or y < 0 or y >= self.height:
                return None, (x, y), passed_through
            passed_through.add((x, y))
            tile = self.grid[y][x]
            if tile == Tile.EMPTY:
                tile = None
            elif (tile == Tile.SPLITTER_VERTICAL and direction in [Direction.NORTH, Direction.SOUTH]) or (tile == Tile.SPLITTER_HORIZONTAL and direction in [Direction.EAST, Direction.WEST]):
                tile = None
        return tile, (x, y), passed_through
    
    def get_next_direction(self, coord: tuple[int, int], direction: Direction) -> list[Direction]:
        tile = self.grid[coord[1]][coord[0]]
        if tile == Tile.SPLITTER_HORIZONTAL:
            if direction in [Direction.NORTH, Direction.SOUTH]:
                return [Direction.EAST, Direction.WEST]
            else:
                return [direction]
        elif tile == Tile.SPLITTER_VERTICAL:
            if direction in [Direction.EAST, Direction.WEST]:
                return [Direction.NORTH, Direction.SOUTH]
            else:
                return [direction]
        elif tile == Tile.MIRROR_FORWARD:
            if direction == Direction.NORTH:
                return [Direction.EAST]
            elif direction == Direction.EAST:
                return [Direction.NORTH]
            elif direction == Direction.SOUTH:
                return [Direction.WEST]
            elif direction == Direction.WEST:
                return [Direction.SOUTH]
        elif tile == Tile.MIRROR_BACKWARD:
            if direction == Direction.NORTH:
                return [Direction.WEST]
            elif direction == Direction.EAST:
                return [Direction.SOUTH]
            elif direction == Direction.SOUTH:
                return [Direction.EAST]
            elif direction == Direction.WEST:
                return [Direction.NORTH]
        else:
            return [direction]
    
    def __str__(self):
        return "\n".join(["".join([char.value for char in line]) for line in self.grid])
    
    def __repr__(self):
        return self.__str__()

    def propagate_light(self, coord: tuple[int, int], direction: Direction) -> set[tuple[int, int]]:
        # print(f"Start propagating: {coord}_{direction} {self.passed_through}")
        hash = f"{coord}_{direction}"
        if hash in self.passed_through:
            # print(f"Already done: {coord}, {direction}")
            return self.passed_through[hash]
        tile, new_coord, passed_through = self.get_next_tile(coord, direction)
        self.passed_through[hash] = passed_through
        if tile is None:
            # print(f"Tile is None ({passed_through})")
            return passed_through
        else:
            next_directions = self.get_next_direction(new_coord, direction)
            # print(f"Directions for next propagations: {next_directions} @ {new_coord}")
            self.passed_through[hash] = passed_through.union(*(self.propagate_light(new_coord, next_direction) for next_direction in next_directions))
            return self.passed_through[hash]


class Assignment(Solution):
    def parse_input(self, input: str, is_gold: bool = False) -> Grid:
        return Grid(input)
    
    def silver(self, input: Grid) -> int:
        return len(input.propagate_light((-1, 0), Direction.EAST))
    
    def gold(self, input: Grid) -> int:
        passed_through = []
        for y in range(input.height):
            # input.passed_through = []
            passed_through.append(len(input.propagate_light((-1, y), Direction.EAST)))
            # input.passed_through = []
            passed_through.append(len(input.propagate_light((input.width, y), Direction.WEST)))

        for x in range(input.width):
            # input.passed_through = []
            passed_through.append(len(input.propagate_light((x, -1), Direction.SOUTH)))
            # input.passed_through = []
            passed_through.append(len(input.propagate_light((x, input.height), Direction.NORTH)))

        return max(passed_through)