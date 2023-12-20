from src.solutions.day_20 import Assignment

sample_input = """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""

second_sample_input = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""


def test_silver():
    input = Assignment().parse_input(sample_input)
    assert Assignment().silver(input=input) == 32000000
    input2 = Assignment().parse_input(second_sample_input)
    assert Assignment().silver(input=input2) == 11687500


def test_gold():
    input = Assignment().parse_input(sample_input, True)
    assert Assignment().gold(input=input) == 0
