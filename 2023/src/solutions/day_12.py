from enum import Enum
from .solution import Solution

class Spring(Enum):
    OPERATIONAL = "."
    BROKEN = "#"
    UNKNOWN = "?"

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.__str__()

class SpringRow:
    def __init__(self, row_str: str) -> None:
        row_split = row_str.split()
        self.springs = [Spring(cell) for cell in row_split[0]]
        self.damaged_sizes = [int(size) for size in row_split[1].split(",")]

    def get_groups(self) -> list[list[Spring]]:
        groups = []
        current_group = []
        for spring in self.springs:
            if spring != Spring.OPERATIONAL:
                current_group.append(spring)
            else:
                if len(current_group) > 0:
                    groups.append(current_group)
                    current_group = []
        if len(current_group) > 0:
            groups.append(current_group)
        return groups


    def get_arrangements(self) -> int:
        groups = self.get_groups()
        if len(groups) == 0:
            return 1
        
        to_check = self.damaged_sizes[:]
        arrangements = 1
        while len(to_check) > 0:
            can_break = False

            if len(groups[0]) == to_check[0]:
                to_check.pop(0)
                groups.pop(0)
            else:
                can_break = True

            if len(groups) == 0 or len(to_check) == 0:
                break

            if len(groups[-1]) == to_check[-1]:
                to_check.pop(-1)
                groups.pop(-1)
            else:
                if can_break:
                    break

        if len(groups) == 0:
            return arrangements

        if len(groups) == 1 and (sum(to_check) + len(to_check) - 1) == len(groups[0]):
            return arrangements

        return arrangements - 1

    def __str__(self) -> str:
        return f"{''.join([str(s) for s in self.springs])} {','.join([str(d) for d in self.damaged_sizes])}"

    def __repr__(self) -> str:
        return self.__str__()


class Assignment(Solution):
    def parse_input(self, input: str, is_gold: bool = False) -> list[SpringRow]:
        return [SpringRow(row) for row in input.split("\n")]
    
    def silver(self, input: list[SpringRow]) -> int:
        print(input)
        for row in input:
            print(row.get_arrangements())
        return 0
    
    def gold(self, input: list[SpringRow]) -> int:
        return 0