from .solution import Solution

def isnumeric(string: str) -> bool:
    try:
        int(string)
        return True
    except ValueError:
        return False
    
def replace_string_numbers(string: str) -> str:
    return string \
        .replace('one', 'one1one') \
        .replace('two', 'two2two') \
        .replace('three', 'three3three') \
        .replace('four', 'four4four') \
        .replace('five', 'five5five') \
        .replace('six', 'six6six') \
        .replace('seven', 'seven7seven') \
        .replace('eight', 'eight8eight') \
        .replace('nine', 'nine9nine') \
        .replace('zero', 'zero0zero')

class Assignment(Solution):
    def parse_input(self, input: str, is_gold: bool = False) -> list[list[int]]:
        if is_gold:
            input = replace_string_numbers(input)
        return [list(map(int, filter(isnumeric, [characters for characters in line]))) for line in input.splitlines()]
    
    def silver(self, input: list[list[int]]) -> int:
        return sum([(calibration_values[0] * 10) + calibration_values[-1] for calibration_values in input])
    
    def gold(self, input: list[list[int]]) -> int:
        return sum([(calibration_values[0] * 10) + calibration_values[-1] for calibration_values in input])