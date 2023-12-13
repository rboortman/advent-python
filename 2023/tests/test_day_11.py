from src.solutions.day_11 import Assignment

sample_input = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""


def test_silver():
    input = Assignment().parse_input(sample_input)
    assert Assignment().silver(input=input) == 374


def test_gold():
    input = Assignment().parse_input(sample_input, True)
    assert Assignment().gold(input=input) == 82000210
