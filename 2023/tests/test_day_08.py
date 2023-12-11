from src.solutions.day_08 import Assignment

sample_input = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""

sample_input_2 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""


def test_silver():
    input = Assignment().parse_input(sample_input)
    assert Assignment().silver(input=input) == 6


def test_gold():
    input = Assignment().parse_input(sample_input_2, True)
    assert Assignment().gold(input=input) == 6
