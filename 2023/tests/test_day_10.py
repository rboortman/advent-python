from src.solutions.day_10 import Assignment

sample_input = """7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ"""


def test_silver():
    input = Assignment().parse_input(sample_input)
    assert Assignment().silver(input=input) == 8


def test_gold():
    input = Assignment().parse_input(sample_input, True)
    assert Assignment().gold(input=input) == 1
