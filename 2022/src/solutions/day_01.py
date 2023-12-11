from .solution import Solution

class Assignment(Solution):
    def parse_input(self, input: str) -> list[int]:
        return [sum(map(int, bag.splitlines())) for bag in input.split('\n\n')]
    
    def silver(self, input: list[int]) -> int:
        return max(input)
    
    def gold(self, input: list[int]) -> int:
        return sum(sorted(input, reverse=True)[:3])