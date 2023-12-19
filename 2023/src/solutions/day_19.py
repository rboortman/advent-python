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


class Memoize:
    def __init__(self, f):
        self.f = f
        self.memo = {}

    def __call__(self, *args):
        if not args in self.memo:
            self.memo[args] = self.f(*args)
        return self.memo[args]


@Memoize
def calculate_possibilities(id: str, instructions: frozenset[Instruction]) -> int:
    instruction = list(filter(lambda x: x.id == id, instructions))[0]
    print(instruction)
    result = 0
    rest_multiplier = 1
    for rule in instruction.rules:
        multiplier = rule[2] - 1 if rule[1] == "<" else 4_000 - rule[2]
        rest_multiplier *= 4_000 - multiplier

        if rule[3] == "R":
            continue
        elif rule[3] == "A":
            result += multiplier
        else:
            result += multiplier * calculate_possibilities(rule[3], instructions)

    if instruction.fallback != "R":
        if instruction.fallback == "A":
            result += rest_multiplier
        else:
            result += rest_multiplier * calculate_possibilities(
                instruction.fallback, instructions
            )

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
        # print(input)
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
        # return 0
        return calculate_possibilities("pv", frozenset(instructions.values()))
