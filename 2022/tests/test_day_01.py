from src.solutions.day_01 import Assignment

sample_input = '''1000
2000
3000

4000

5000
6000

7000
8000
9000

10000'''

def test_silver():
    input = Assignment().parse_input(sample_input)
    assert Assignment().silver(input=input) == 24000
    
def test_gold():
    input = Assignment().parse_input(sample_input)
    assert Assignment().gold(input=input) == 45000