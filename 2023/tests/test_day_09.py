from src.solutions.day_09 import Assignment

sample_input = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""


def test_silver():
    input = Assignment().parse_input(sample_input)
    assert Assignment().silver(input=input) == 114


def test_gold():
    input = Assignment().parse_input(sample_input, True)
    assert Assignment().gold(input=input) == 2
