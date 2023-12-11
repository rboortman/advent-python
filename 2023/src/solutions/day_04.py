from .solution import Solution

class ScratchCard:
    def __init__(self, winning_numbers: list[int], numbers: list[int]) -> None:
        self.winning_numbers = winning_numbers
        self.numbers = numbers
        
    def __repr__(self) -> str:
        return f"({self.winning_numbers}, {self.numbers})"
    
    def get_won_numbers(self) -> list[int]:
        return [number for number in self.numbers if number in self.winning_numbers]
    
    def get_score(self) -> int:
        length = len(self.get_won_numbers()) - 1
        if length < 0:
            return 0
        return 2 ** length
        

class Assignment(Solution):
    def parse_input(self, input: str, is_gold: bool = False) -> list[ScratchCard]:
        cards = []
        for line in input.splitlines():
            index = line.find(":")
            line = line[index + 2:]
            winning_numbers, numbers = line.split("|")
            cards.append(ScratchCard([int(number) for number in winning_numbers.strip().split(" ") if len(number) > 0], [int(number) for number in numbers.strip().split(" ") if len(number) > 0]))
        return cards
    
    def silver(self, input: list[ScratchCard]) -> int:
        return sum(map(ScratchCard.get_score, input))
    
    def gold(self, input: list[ScratchCard]) -> int:
        conversion = list(map(lambda card: len(card.get_won_numbers()), input))
        cards_exploded = [1 for _ in range(len(input))]
        for i, won in enumerate(conversion):
            for _ in range(cards_exploded[i]):
                for k in range(won):
                    cards_exploded[i+k+1] += 1
                
        return sum(cards_exploded)