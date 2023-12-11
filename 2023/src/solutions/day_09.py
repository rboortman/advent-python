import math
from .solution import Solution


class Sequence:
    def __init__(self, sequence: str) -> None:
        self.initial_sequence = list(map(int, sequence.split()))
        self.all_sequences = [self.initial_sequence]
        self.parse_sequence()

    def parse_sequence(self) -> None:
        last_sequence = self.initial_sequence
        while last_sequence[0] != last_sequence[1] or sum(last_sequence) != 0:
            last_sequence = [
                last_sequence[i + 1] - last_sequence[i]
                for i in range(len(last_sequence) - 1)
            ]
            self.all_sequences.append(last_sequence)

    def find_more_history(self) -> int:
        last_found = 0
        for sequence in self.all_sequences[::-1]:
            sequence.insert(0, sequence[0] - last_found)
            last_found = sequence[0]
        return last_found

    def __len__(self) -> int:
        return len(self.initial_sequence)

    def __getitem__(self, index: int) -> int:
        if len(self.initial_sequence) > index:
            return self.initial_sequence[index]

        last_found = 0
        for _ in range(index - len(self.initial_sequence) + 1):
            last_found = 0
            for sequence in self.all_sequences[::-1]:
                sequence.append(sequence[-1] + last_found)
                last_found = sequence[-1]
        return last_found

    def __str__(self) -> str:
        sequence_str = ""
        max_length = max(
            len(str(max(self.all_sequences[0]))), len(str(min(self.all_sequences[0])))
        )
        right_padding = math.floor(max_length / 2)
        for i, sequence in enumerate(self.all_sequences):
            sequence_str += f"{' '.join([''] * (i + 1))}{'  '.join([str(s).rjust(right_padding).ljust(max_length) for s in sequence])}\n"
        return sequence_str

    def __repr__(self) -> str:
        return self.__str__()


class Assignment(Solution):
    def parse_input(self, input: str, is_gold: bool = False) -> list[Sequence]:
        return [Sequence(sequence) for sequence in input.splitlines()]

    def silver(self, input: list[Sequence]) -> int:
        return sum([sequence[len(sequence)] for sequence in input])

    def gold(self, input: list[Sequence]) -> int:
        return sum([sequence.find_more_history() for sequence in input])
