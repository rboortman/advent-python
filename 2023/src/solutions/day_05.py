from .solution import Solution

class Converter:
    def __init__(self, input: str) -> None:
        parsed = list(map(int, input.split()))
        self.source_start = parsed[1]
        self.source_end = parsed[1] + parsed[2]
        self.dest_start = parsed[0]
        self.dest_end = parsed[0] + parsed[2]
        self.diff = parsed[0] - parsed[1]
        
    def is_in_range(self, number: int) -> bool:
        return number >= self.source_start and number <= self.source_end
    
    def is_in_dest_range(self, number: int) -> bool:
        return number >= self.dest_start and number <= self.dest_end
    
    def convert(self, number: int) -> int:
        if not self.is_in_range(number):
            return NotImplemented
        return number + self.diff
    
    def convert_back(self, number: int) -> int:
        if not self.is_in_dest_range(number):
            return NotImplemented
        return number - self.diff
    
    def __repr__(self) -> str:
        return f"([{self.source_start}, {self.source_end}], {self.diff})"
    
    def __str__(self) -> str:
        return f"([{self.source_start}, {self.source_end}], {self.diff})"
    
class Collection:
    def __init__(self, id: str, input: str) -> None:
        self.id = id
        self.converters = []
        for line in input.splitlines():
            self.converters.append(Converter(input=line))
            
    def convert(self, number: int) -> int:
        for converter in self.converters:
            if converter.is_in_range(number):
                return converter.convert(number)
        return number
    
    def convert_back(self, number: int) -> int:
        for converter in self.converters:
            if converter.is_in_dest_range(number):
                return converter.convert_back(number)
        return number
    
    def get_top_range(self) -> int:
        return max(map(lambda converter: converter.source_end, self.converters))
    
    def get_top_dest_range(self) -> int:
        return max(map(lambda converter: converter.dest_end, self.converters))
    
    def __repr__(self) -> str:
        converter_strings = "\n".join([str(converter) for converter in self.converters])
        return f"{self.id}\n{converter_strings}\n"
        

class Assignment(Solution):
    def parse_input(self, input: str, is_gold: bool = False) -> tuple[list[Collection], list[int]]:
        input = input.split("\n\n")
        seeds = list(map(int, input[0][7:].split()))
        collections = []
        for collection_str in input[1:]:
            collection_split = collection_str.split("\n", maxsplit=1)
            collections.append(Collection(id=collection_split[0], input=collection_split[1]))
        return (collections, seeds)
    
    def silver(self, input: tuple[list[Collection], list[int]]) -> int:
        locations = []
        for seed in input[1]:
            for collection in input[0]:
                seed = collection.convert(seed)
            locations.append(seed)
        return min(locations)
    
    def gold(self, input: tuple[list[Collection], list[int]]) -> int:
        seeds = [(input[1][i*2], input[1][i*2] + input[1][i*2+1]) for i in range(int(len(input[1])/2))]
        collections = input[0]
        top = collections[-1].get_top_dest_range()
        print(top, seeds)
        for i in range(top):
            seed_id = i
            for collection in collections[::-1]:
                seed_id = collection.convert_back(seed_id)
            if i % 100000 == 0:
                print(i)
            for seed in seeds:
                if seed[0] <= seed_id <= seed[1]:
                    return i