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
        arrangements = 1
        if len(groups) == 0:
            return arrangements

        to_check = self.damaged_sizes[:]
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

        if len(groups) == len(to_check):
            sub_arrangements = 1
            print(groups, to_check)
            for i, group in enumerate(groups):
                if len(group) != to_check[i]:
                    try:
                        first_part = group.index(Spring.BROKEN)
                        last_part = max(
                            i for i, val in enumerate(group) if val == Spring.BROKEN
                        )
                        sub_arrangements *= to_check[i] - (last_part - first_part)
                    except ValueError:
                        sub_arrangements *= len(group) - (to_check[i] - 1)
            return sub_arrangements

        return arrangements - 1

    def is_valid_combination(self, combination: list[Spring]) -> bool:
        to_check = self.damaged_sizes[:]
        broken_size = 0
        for i, spring in enumerate(combination):
            if self.springs[i] != Spring.UNKNOWN and self.springs[i] != spring:
                return False

            if spring == Spring.BROKEN:
                broken_size += 1
                if broken_size > to_check[0]:
                    return False

            else:
                if broken_size <= 0:
                    continue
                if broken_size == to_check[0]:
                    to_check.pop(0)
                    broken_size = 0
                else:
                    return False

        return True

    def get_all_combinations(self) -> list[list[Spring]]:
        total_broken = sum([1 for spring in self.springs if spring == Spring.BROKEN])
        total_unknown = sum([1 for spring in self.springs if spring == Spring.UNKNOWN])
        all_broken = [
            Spring.BROKEN for _ in range(sum(self.damaged_sizes) - total_broken)
        ]
        all_operational = [
            Spring.OPERATIONAL for _ in range(total_unknown - len(all_broken))
        ]
        perm = permutations(all_broken + all_operational)

        unknown_indices = [
            i for i, spring in enumerate(self.springs) if spring == Spring.UNKNOWN
        ]
        valid_combinations = []
        checked_combinations = dict()
        for p in perm:
            if p in checked_combinations:
                continue
            checked_combinations[p] = True

            combination = self.springs[:]
            for i, index in enumerate(unknown_indices):
                combination[index] = p[i]
            if self.is_valid_combination(combination):
                valid_combinations.append(combination)
        return len(valid_combinations)

    def get_bruteforce_arrangements(self) -> int:
        groups = self.get_groups()

    def __str__(self) -> str:
        return f"{''.join([str(s) for s in self.springs])} {','.join([str(d) for d in self.damaged_sizes])}"

    def __repr__(self) -> str:
        return self.__str__()


class Assignment(Solution):
    def parse_input(self, input: str, is_gold: bool = False) -> list[SpringRow]:
        return [SpringRow(row) for row in input.split("\n")]

    def silver(self, input: list[SpringRow]) -> int:
        s = 0
        for i, row in enumerate(input):
            print(i)
            s += row.get_all_combinations()
        return s
        # return sum([row.get_all_combinations() for row in input])

    def gold(self, input: list[SpringRow]) -> int:
        return 0
