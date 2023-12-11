import math
from .solution import Solution

class Assignment(Solution):
    def parse_input(self, input: str, is_gold: bool = False) -> list[tuple[int, int]]:
        input = input.splitlines()
        input[0] = input[0][11:]
        input[1] = input[1][11:]
        if is_gold:
            input[0] = input[0].replace(' ', '')
            input[1] = input[1].replace(' ', '')
        times = list(map(int, input[0].split()))
        distances = list(map(int, input[1].split()))
        return list(map(lambda x: (x[0], x[1]), zip(times, distances)))
    
    def silver(self, input: list[tuple[int, int]]) -> int:
        return math.prod(map(lambda x: len([i*(x[0] - i) for i in range(x[0]) if i*(x[0] - i) > x[1]]), input))
    
    def gold(self, input: list[tuple[int, int]]) -> int:
        time = input[0][0]
        distances = input[0][1]
        for i in range(time):
            if i*(time - i) > distances:
                return time - (i * 2) + 1
        return 0