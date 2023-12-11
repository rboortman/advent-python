from src.solutions.day_06 import Assignment

sample_input = '''Time:      7  15   30
Distance:  9  40  200'''

def test_silver():
    input = Assignment().parse_input(sample_input)
    assert Assignment().silver(input=input) == 288
    
def test_gold():
    input = Assignment().parse_input(sample_input, True)
    assert Assignment().gold(input=input) == 71503