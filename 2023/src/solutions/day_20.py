from .solution import Solution



class Assignment(Solution):
    def parse_input(self, input: str, is_gold: bool = False) -> str:
        return input
    
    def silver(self, input: str) -> int:
        print(input)
        return 0
    
    def gold(self, input: str) -> int:
        return 0