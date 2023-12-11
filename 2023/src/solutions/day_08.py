import math
from enum import Enum
from .solution import Solution


class Instruction(Enum):
    Left = 0
    Right = 1


class Assignment(Solution):
    def parse_input(
        self, input: str, is_gold: bool = False
    ) -> tuple[list[Instruction], dict[str, tuple[str, str]]]:
        input = input.split("\n\n")
        instructions = [
            Instruction.Left if i == "L" else Instruction.Right for i in input[0]
        ]
        maze = {}
        for line in input[1].splitlines():
            line = line.split()
            maze[line[0]] = (line[2][1:-1], line[3][:-1])
        return (instructions, maze)

    def silver(
        self, input: tuple[list[Instruction], dict[str, tuple[str, str]]]
    ) -> int:
        instructions, maze = input
        room = "AAA"
        steps = 0
        while room != "ZZZ":
            instruction = instructions[steps % len(instructions)]
            room = maze[room][instruction.value]
            steps += 1
        return steps

    def gold(self, input: tuple[list[Instruction], dict[str, tuple[str, str]]]) -> int:
        instructions, maze = input
        rooms = [room for room in list(maze.keys()) if room[2] == "A"]
        steps_list = []
        for room in rooms:
            steps = 0
            while room[2] != "Z":
                instruction = instructions[steps % len(instructions)]
                room = maze[room][instruction.value]
                steps += 1
            steps_list.append(steps)
        print(steps_list)

        return math.lcm(*steps_list)
