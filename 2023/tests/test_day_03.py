from src.solutions.day_03 import Assignment

sample_input = '''467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..'''

def test_silver():
    input = Assignment().parse_input(sample_input)
    assert Assignment().silver(input=input) == 4361
    
def test_gold():
    input = Assignment().parse_input(sample_input, True)
    assert Assignment().gold(input=input) == 467835