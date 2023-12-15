from enum import Enum
from .solution import Solution


class Operation(Enum):
    REMOVE = 0
    INSERT = 1

class Step:
    def __init__(self, input: str):
        self.input = input
        if self.input[-1] == "-":
            self.operation = Operation.REMOVE
            self.label = self.input[:-1]
        else:
            self.operation = Operation.INSERT
            split_input = self.input.split("=")
            self.lens = Lens(split_input[0], int(split_input[1]))
            self.label = self.lens.label
        
        self.label_hash = self.get_label_hash()
        

    def get_hash(self):
        result = 0
        for char in self.input:
            result = ((result + ord(char)) * 17) % 256
        return result

    def get_label_hash(self):
        result = 0
        for char in self.label:
            result = ((result + ord(char)) * 17) % 256
        return result

    def __str__(self):
        return self.input
    
    def __repr__(self):
        return self.__str__()
    
class Lens:
    def __init__(self, label: str, size: int):
        self.label = label
        self.size = size

    def __str__(self):
        return f"[{self.label}: {self.size}]"
    
    def __repr__(self):
        return self.__str__()


class Assignment(Solution):
    def parse_input(self, input: str, is_gold: bool = False) -> list[Step]:
        return [Step(i) for i in input.split(",")]
    
    def silver(self, input: list[Step]) -> int:
        return sum([i.get_hash() for i in input])
    
    def gold(self, input: list[Step]) -> int:
        boxes = [[] for _ in range(265)]
        for step in input:
            if step.operation == Operation.REMOVE:
                for (i, lens) in enumerate(boxes[step.label_hash]):
                    if lens.label == step.label:
                        boxes[step.label_hash] = boxes[step.label_hash][:i] + boxes[step.label_hash][i + 1:]
                        break
            else:
                for lens in boxes[step.label_hash]:
                    if lens.label == step.label:
                        lens.size = step.lens.size
                        break
                else:
                    boxes[step.label_hash].append(step.lens)

        # for (i, box) in enumerate(boxes):
        #     print(f"Box {str(i).rjust(3, ' ')}: {box}")
        # return 0
        return sum([(i + 1) * (j + 1) * lens.size for (i, box) in enumerate(boxes) if len(box) > 0 for (j, lens) in enumerate(box)])