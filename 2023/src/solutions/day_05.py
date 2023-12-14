from .solution import Solution

class Converter:
    def __init__(self, input: str) -> None:
        parsed = list(map(int, input.split()))
        self.source_start = parsed[1]
        self.source_end = parsed[1] + parsed[2] - 1
        self.dest_start = parsed[0]
        self.dest_end = parsed[0] + parsed[2] - 1
        self.diff = parsed[0] - parsed[1]
        
    def is_in_range(self, number: int) -> bool:
        return number >= self.source_start and number <= self.source_end
    
    def is_in_dest_range(self, number: int) -> bool:
        return number >= self.dest_start and number <= self.dest_end
    
    def convert(self, number: int) -> int:
        if not self.is_in_range(number):
            return number
        return number + self.diff
    
    def convert_back(self, number: int) -> int:
        if not self.is_in_dest_range(number):
            return number
        return number - self.diff
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __str__(self) -> str:
        return f"([{self.source_start:_}, {self.source_end:_}] -> [{self.dest_start:_}, {self.dest_end:_}], {self.diff:_})"
    
class Collection:
    def __init__(self, id: str, input: str) -> None:
        self.id = id
        self.converters = []
        for line in input.splitlines():
            self.converters.append(Converter(input=line))
        self.converters = sorted(self.converters, key=lambda converter: converter.source_start)
            
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
    
    def map_ranges(self, ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
        sorted_converters = sorted(self.converters, key=lambda converter: converter.source_start)
        new_ranges = []
        for (start, end) in ranges:
            if end < sorted_converters[0].source_start or start > sorted_converters[-1].source_end:
                new_ranges.append((start, end))
            else:
                if start < sorted_converters[0].source_start:
                    new_ranges.append((start, sorted_converters[0].source_start - 1))
                if end > sorted_converters[-1].source_end:
                    new_ranges.append((sorted_converters[-1].source_end + 1, end))

            for (index, converter) in enumerate(sorted_converters):
                if converter.source_end < start or converter.source_start > end:
                    continue
                dest_start = converter.convert(max(start, converter.source_start))
                dest_end = converter.convert(min(end, converter.source_end))
                new_ranges.append((dest_start, dest_end))

                if index < len(sorted_converters) - 1:
                    next_converter = sorted_converters[index+1]
                    if next_converter.source_start > converter.source_end + 1:
                        new_ranges.append((converter.source_end + 1, next_converter.source_start - 1))
        return new_ranges
    
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

        ranges = seeds
        for collection in collections:
            ranges = collection.map_ranges(ranges)

        return min([seed[0] for seed in ranges])