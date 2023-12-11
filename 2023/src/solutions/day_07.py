from enum import Enum
from typing import Final
from .solution import Solution

class CardStrength(Enum):
    TWO = '2'
    THREE = '3'
    FOUR = '4'
    FIVE = '5'
    SIX = '6'
    SEVEN = '7'
    EIGHT = '8'
    NINE = '9'
    TEN = 'T'
    JACK = 'J'
    QUEEN = 'Q'
    KING = 'K'
    ACE = 'A'
    
class CardType(Enum):
    FIVE_OF_A_KIND = 10
    FOUR_OF_A_KIND = 9
    FULL_HOUSE = 8
    THREE_OF_A_KIND = 7
    TWO_PAIR = 6
    ONE_PAIR = 5
    HIGH_CARD = 4
    
STRENGTH_ORDER: Final[list[CardStrength]] = [
    CardStrength.TWO,
    CardStrength.THREE,
    CardStrength.FOUR,
    CardStrength.FIVE,
    CardStrength.SIX,
    CardStrength.SEVEN,
    CardStrength.EIGHT,
    CardStrength.NINE,
    CardStrength.TEN,
    CardStrength.JACK,
    CardStrength.QUEEN,
    CardStrength.KING,
    CardStrength.ACE
]
    
STRENGTH_ORDER_GOLD: Final[list[CardStrength]] = [
    CardStrength.JACK,
    CardStrength.TWO,
    CardStrength.THREE,
    CardStrength.FOUR,
    CardStrength.FIVE,
    CardStrength.SIX,
    CardStrength.SEVEN,
    CardStrength.EIGHT,
    CardStrength.NINE,
    CardStrength.TEN,
    CardStrength.QUEEN,
    CardStrength.KING,
    CardStrength.ACE
]

class Hand:
    def __init__(self, cards: list[str], bid: int, is_gold: bool = False) -> None:
        self.cards = cards
        self.bid = bid
        self.gold = is_gold
        self.card_type = self.get_card_type()
        
    def get_card_type(self) -> CardType:
        if self.gold:
            count_j = self.cards.count(CardStrength.JACK)
            filtered_cards = [card for card in self.cards if card != CardStrength.JACK]
            set_count = len(set(filtered_cards))
            
            match count_j:
                case 5 | 4:
                    return CardType.FIVE_OF_A_KIND
                case 3:
                    if set_count == 1:
                        return CardType.FIVE_OF_A_KIND
                    return CardType.FOUR_OF_A_KIND
                case 2:
                    if set_count == 1:
                        return CardType.FIVE_OF_A_KIND
                    elif set_count == 2:
                        return CardType.FOUR_OF_A_KIND
                    return CardType.THREE_OF_A_KIND
                case 1:
                    if set_count == 1:
                        return CardType.FIVE_OF_A_KIND
                    elif set_count == 2:
                        if filtered_cards.count(filtered_cards[0]) == 2:
                            return CardType.FULL_HOUSE
                        return CardType.FOUR_OF_A_KIND
                    elif set_count == 3:
                        return CardType.THREE_OF_A_KIND
                    elif set_count == 4:
                        return CardType.ONE_PAIR
            
        count_0 = self.cards.count(self.cards[0])
        count_1 = self.cards.count(self.cards[1])
        count_2 = self.cards.count(self.cards[2])
        count_3 = self.cards.count(self.cards[3])
        count_4 = self.cards.count(self.cards[4])
        
        if count_0 == 5:
            return CardType.FIVE_OF_A_KIND
        elif count_0 == 4 or count_1 == 4:
            return CardType.FOUR_OF_A_KIND
        elif count_0 == 3 or count_1 == 3 or count_2 == 3:
            if count_0 == 2 or count_1 == 2 or count_2 == 2 or count_3 == 2:
                return CardType.FULL_HOUSE
            return CardType.THREE_OF_A_KIND
        elif count_0 == 1 and count_1 == 1 and count_2 == 1 and count_3 == 1 and count_4 == 1:
            return CardType.HIGH_CARD
        else:
            if len(set(self.cards)) == 4:
                return CardType.ONE_PAIR
            elif len(set(self.cards)) == 3:
                return CardType.TWO_PAIR
    
    def __lt__(self, other: 'Hand') -> bool:
        if self.card_type.value < other.card_type.value:
            return True
        elif self.card_type.value > other.card_type.value:
            return False
        
        strength_order = STRENGTH_ORDER_GOLD if self.gold else STRENGTH_ORDER

        for i in range(len(self.cards)):
            if strength_order.index(self.cards[i]) < strength_order.index(other.cards[i]):
                return True
            elif strength_order.index(self.cards[i]) > strength_order.index(other.cards[i]):
                return False
        return False
    
    def __gt__(self, other: 'Hand') -> bool:
        if self.card_type.value > other.card_type.value:
            return True
        elif self.card_type.value < other.card_type.value:
            return False
        
        strength_order = STRENGTH_ORDER_GOLD if self.gold else STRENGTH_ORDER
        
        for i in range(len(self.cards)):
            if strength_order.index(self.cards[i]) > strength_order.index(other.cards[i]):
                return True
            elif strength_order.index(self.cards[i]) < strength_order.index(other.cards[i]):
                return False
        return False
    
    def __eq__(self, other: 'Hand') -> bool:
        if self.card_type.value != other.card_type.value:
            return False
        
        strength_order = STRENGTH_ORDER_GOLD if self.gold else STRENGTH_ORDER
        
        for i in range(len(self.cards)):
            if strength_order.index(self.cards[i]) != strength_order.index(other.cards[i]):
                return False
        return True
    
    def __le__(self, other: 'Hand') -> bool:
        if self.card_type.value > other.card_type.value:
            return False
        elif self.card_type.value < other.card_type.value:
            return True
        
        strength_order = STRENGTH_ORDER_GOLD if self.gold else STRENGTH_ORDER
        
        for i in range(len(self.cards)):
            if strength_order.index(self.cards[i]) > strength_order.index(other.cards[i]):
                return False
            elif strength_order.index(self.cards[i]) < strength_order.index(other.cards[i]):
                return True
        return True
    
    def __ge__(self, other: 'Hand') -> bool:
        if self.card_type.value < other.card_type.value:
            return False
        elif self.card_type.value > other.card_type.value:
            return True
        
        strength_order = STRENGTH_ORDER_GOLD if self.gold else STRENGTH_ORDER
        
        for i in range(len(self.cards)):
            if strength_order.index(self.cards[i]) < strength_order.index(other.cards[i]):
                return False
            elif strength_order.index(self.cards[i]) > strength_order.index(other.cards[i]):
                return True
        return True
    
    def __ne__(self, other: 'Hand') -> bool:
        if self.card_type.value == other.card_type.value:
            return False
        
        strength_order = STRENGTH_ORDER_GOLD if self.gold else STRENGTH_ORDER
        
        for i in range(len(self.cards)):
            if strength_order.index(self.cards[i]) == strength_order.index(other.cards[i]):
                return False
        return True
    
    def __str__(self) -> str:
        return f'HAND\n----\nCards:   {self.cards}\nStrength: {self.card_type}\nBid:      {self.bid}\n----\n'
    
    def __repr__(self) -> str:
        return self.__str__()


class Assignment(Solution):
    def parse_input(self, input: str, is_gold: bool = False) -> list[Hand]:
        return list(map(lambda x: Hand([CardStrength(c) for c in x.split()[0]], int(x.split()[-1]), is_gold), input.splitlines()))
    
    def silver(self, input: list[Hand]) -> int:
        input.sort()
        return sum([hand.bid * (index + 1) for (index, hand) in enumerate(input)])
    
    def gold(self, input: list[Hand]) -> int:
        input.sort()
        return sum([hand.bid * (index + 1) for (index, hand) in enumerate(input)])