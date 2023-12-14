from enum import Enum
from itertools import permutations
from .solution import Solution

class Spring(Enum):
    OPERATIONAL = "."
    BROKEN = "#"
    UNKNOWN = "?"

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.__str__()
    
    def __hash__(self) -> int:
        return hash(self.value)
        # return super().__hash__()


class SpringRow:
    def __init__(self, row_str: str, is_gold: bool = False) -> None:
        row_split = row_str.split()
        self.springs = [Spring(cell) for cell in row_split[0]]
        if is_gold:
            self.springs = (self.springs + [Spring.UNKNOWN]) * 5
            self.springs = self.springs[0:-1]
        self.damaged_sizes = [int(size) for size in row_split[1].split(",")]
        if is_gold:
            self.damaged_sizes = self.damaged_sizes * 5
    

class Memoize:
    def __init__(self, f):
        self.f = f
        self.memo = {}
    def __call__(self, *args):
        if not args in self.memo:
            self.memo[args] = self.f(*args)
        return self.memo[args]
    
@Memoize
def get_arrangements(line: tuple[Spring], to_check: tuple[int], check_left: int) -> int:
    if len(line) == 0:
        return 1 if len(to_check) == 0 and check_left <= 0 else 0
    
    if check_left > 0:
        if line[0] == Spring.BROKEN or line[0] == Spring.UNKNOWN:
            return get_arrangements(line[1:], to_check, check_left - 1)
        else:
            return 0
        
    if check_left == 0:
        if len(to_check) == 0:
            try:
                next(val for val in line if val == Spring.BROKEN)
                return 0
            except StopIteration:
                return 1
        else:
            if line[0] == Spring.BROKEN:
                return 0
            else:
                return get_arrangements(line[1:], to_check, -1)
            
    if check_left < 0:
        if line[0] == Spring.OPERATIONAL:
            return get_arrangements(line[1:], to_check, -1)
        elif line[0] == Spring.BROKEN:
            return get_arrangements(line[1:], to_check[1:], to_check[0] - 1)
        else:
            return get_arrangements(line[1:], to_check[1:], to_check[0] - 1) + get_arrangements(line[1:], to_check, -1)


class Assignment(Solution):
    def parse_input(self, input: str, is_gold: bool = False) -> list[SpringRow]:
        return [SpringRow(row, is_gold=is_gold) for row in input.split("\n")]

    def silver(self, input: list[SpringRow]) -> int:
        return sum([get_arrangements(tuple(row.springs), tuple(row.damaged_sizes), -1) for row in input])

    def gold(self, input: list[SpringRow]) -> int:
        a = [get_arrangements(tuple(row.springs), tuple(row.damaged_sizes), -1) for row in input]
        return sum(a)
