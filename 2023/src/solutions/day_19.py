import math
from .solution import Solution


class Gear:
    def __init__(self, input: str) -> None:
        self.values = [int(x[x.index("=") + 1 :]) for x in input[1:-1].split(",")]

    def __str__(self) -> str:
        return str(self.values)

    def __repr__(self) -> str:
        return self.__str__()


class Instruction:
    def __init__(self, input: str) -> None:
        first_delim = input.index("{")
        self.id = input[:first_delim]
        rules = []
        for rule_str in input[first_delim + 1 : -1].split(","):
            if ":" not in rule_str:
                self.fallback = rule_str
            else:
                rule_split = rule_str.split(":")
                if ">" in rule_split[0]:
                    condition_split = rule_split[0].split(">") + [">"]
                else:
                    condition_split = rule_split[0].split("<") + ["<"]
                index = 0
                if condition_split[0] == "m":
                    index = 1
                elif condition_split[0] == "a":
                    index = 2
                elif condition_split[0] == "s":
                    index = 3

                rules.append(
                    (
                        index,
                        condition_split[2],
                        int(condition_split[1]),
                        rule_split[1],
                    )
                )
        self.rules = rules

    def parse_gear(self, gear: Gear) -> str:
        for rule in self.rules:
            if rule[1] == "<":
                if gear.values[rule[0]] < rule[2]:
                    return rule[3]
            else:
                if gear.values[rule[0]] > rule[2]:
                    return rule[3]
        return self.fallback

    def __str__(self) -> str:
        to_print = self.id + " {\n"
        for rule in self.rules:
            to_print += f"  {rule[0]}{rule[1]}{rule[2]}: {rule[3]},\n"
        to_print += "}\n"
        to_print += f"fallback: {self.fallback}\n"
        return to_print

    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self) -> int:
        return hash(self.__str__())


def get_xmas(rule: tuple[int, str, int, str], x: tuple[int, int], m: tuple[int, int], a: tuple[int, int], s: tuple[int, int]) -> tuple[int, tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]:
    xmas = [(x[1] - x[0]), (m[1] - m[0]), (a[1] - a[0]), (s[1] - s[0])]
    return math.prod(xmas), x, m, a, s

class Memoize:
    def __init__(self, f):
        self.f = f
        self.memo = {}

    def __call__(self, *args):
        if not args in self.memo:
            self.memo[args] = self.f(*args)
        return self.memo[args]


@Memoize
def calculate_possibilities(id: str, instructions: frozenset[Instruction], x: tuple[int, int] = (0, 4_000), m: tuple[int, int] = (0, 4_000), a: tuple[int, int] = (0, 4_000), s: tuple[int, int] = (0, 4_000)) -> int:
    instruction = list(filter(lambda x: x.id == id, instructions))[0]
    result = 0
    for rule in instruction.rules:
        alt_x, alt_m, alt_a, alt_s = x, m, a, s
        if rule[0] == 0:
            if (rule[1] == "<" and rule[2] < x[0]) or (rule[1] == ">" and rule[2] > x[1]):
                continue
            else:
                if rule[1] == "<":
                    alt_x = (x[0], max(x[0], rule[2] - 1))
                    x = (min(x[1], rule[2] - 1), x[1])
                elif rule[1] == ">":
                    alt_x = (min(x[1], rule[2]), x[1])
                    x = (x[0], max(x[0], rule[2]))
        elif rule[0] == 1:
            if (rule[1] == "<" and rule[2] < m[0]) or (rule[1] == ">" and rule[2] > m[1]):
                continue
            else:
                if rule[1] == "<":
                    alt_m = (m[0], max(m[0], rule[2] - 1))
                    m = (min(m[1], rule[2] - 1), m[1])
                elif rule[1] == ">":
                    alt_m = (min(m[1], rule[2]), m[1])
                    m = (m[0], max(m[0], rule[2]))
        elif rule[0] == 2:
            if (rule[1] == "<" and rule[2] < a[0]) or (rule[1] == ">" and rule[2] > a[1]):
                continue
            else:
                if rule[1] == "<":
                    alt_a = (a[0], max(a[0], rule[2] - 1))
                    a = (min(a[1], rule[2] - 1), a[1])
                elif rule[1] == ">":
                    alt_a = (min(a[1], rule[2]), a[1])
                    a = (a[0], max(a[0], rule[2]))
        elif rule[0] == 3:
            if (rule[1] == "<" and rule[2] < s[0]) or (rule[1] == ">" and rule[2] > s[1]):
                continue
            else:
                if rule[1] == "<":
                    alt_s = (s[0], max(s[0], rule[2] - 1))
                    s = (min(s[1], rule[2] - 1), s[1])
                elif rule[1] == ">":
                    alt_s = (min(s[1], rule[2]), s[1])
                    s = (s[0], max(s[0], rule[2]))

        if rule[3] == "R":
            continue
        elif rule[3] == "A":
            result += (alt_x[1] - alt_x[0]) * (alt_m[1] - alt_m[0]) * (alt_a[1] - alt_a[0]) * (alt_s[1] - alt_s[0])
        else:
            result += calculate_possibilities(rule[3], instructions, alt_x, alt_m, alt_a, alt_s)

    if instruction.fallback != "R":
        if instruction.fallback == "A":
            result += (x[1] - x[0]) * (m[1] - m[0]) * (a[1] - a[0]) * (s[1] - s[0])
        else:
            result += calculate_possibilities(instruction.fallback, instructions, x, m, a, s)

    return result


class Assignment(Solution):
    def parse_input(
        self, input: str, is_gold: bool = False
    ) -> tuple[dict[str, Instruction], list[Gear]]:
        input_split = input.split("\n\n")
        return (
            {
                instruction.id: instruction
                for instruction in [Instruction(x) for x in input_split[0].splitlines()]
            },
            [Gear(x) for x in input_split[1].splitlines()],
        )

    def silver(self, input: tuple[dict[str, Instruction], list[Gear]]) -> int:
        instructions, gears = input
        result = 0
        for gear in gears:
            state = "in"
            while state != "R" and state != "A":
                state = instructions[state].parse_gear(gear)
            if state == "A":
                result += sum(gear.values)
        return result

    def gold(self, input: tuple[dict[str, Instruction], list[Gear]]) -> int:
        instructions, _ = input
        return calculate_possibilities("in", frozenset(instructions.values()))
