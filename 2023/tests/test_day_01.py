from src.solutions.day_01 import Assignment

sample_input = '''1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet'''

sample_input_gold = '''two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen'''

def test_silver():
    input = Assignment().parse_input(sample_input)
    assert Assignment().silver(input=input) == 142
    
def test_gold():
    input = Assignment().parse_input(sample_input_gold, True)
    assert Assignment().gold(input=input) == 281