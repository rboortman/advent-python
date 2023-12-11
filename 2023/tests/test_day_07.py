from src.solutions.day_07 import Assignment

sample_input = '''32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483'''

def test_silver():
    input = Assignment().parse_input(sample_input)
    assert Assignment().silver(input=input) == 6440
    
def test_gold():
    input = Assignment().parse_input(sample_input, True)
    assert Assignment().gold(input=input) == 5905