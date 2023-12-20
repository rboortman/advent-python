from enum import Enum
from .solution import Solution


class Signal(Enum):
    HIGH = 1
    LOW = 0

    def __str__(self) -> str:
        return str(f"-{self.name}->")
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __invert__(self) -> "Signal":
        return Signal(1 - self.value)
    
    def __and__(self, other: "Signal") -> "Signal":
        return Signal(self.value & other.value)
    
    def __or__(self, other: "Signal") -> "Signal":
        return Signal(self.value | other.value)
    
    def __xor__(self, other: "Signal") -> "Signal":
        return Signal(self.value ^ other.value)
    
class ModuleType(Enum):
    BUTTON = "button"
    BROADCASTER = "broadcaster"
    FLIP_FLOP = "%"
    CONJUNCTION = "&"

class Module:
    def __init__(self, input: str) -> None:
        input_output = input.split(" -> ")
        if input_output[0] == ModuleType.BUTTON.value:
            self.id = input_output[0]
            self.input = []
            self.type = ModuleType.BUTTON
            self.output = input_output[1].split(", ")
        elif input_output[0] == ModuleType.BROADCASTER.value:
            self.id = input_output[0]
            self.input = []
            self.type = ModuleType.BROADCASTER
            self.output = input_output[1].split(", ")
        else:
            self.id = input_output[0][1:]
            self.type = ModuleType(input_output[0][0])
            self.input = []
            self.output = input_output[1].split(", ")

        if self.type == ModuleType.FLIP_FLOP:
            self.on = False

        if self.type == ModuleType.CONJUNCTION:
            self.memory = dict()

    def add_input(self, input: list[str]) -> "Module":
        self.input += input
        if self.type == ModuleType.CONJUNCTION:
            for i in input:
                self.memory[i] = Signal.LOW
        return self

    def process_signal(self, signal: Signal, source: str) -> (Signal, list[str]):
        out_signal = None
        if self.type == ModuleType.BUTTON or self.type == ModuleType.BROADCASTER:
            out_signal = signal
        elif self.type == ModuleType.FLIP_FLOP:
            if signal == Signal.LOW:
                self.on = not self.on
                out_signal = Signal(self.on)
        elif self.type == ModuleType.CONJUNCTION:
            self.memory[source] = signal
            if all(self.memory.values()):
                out_signal = Signal.LOW
            else:
                out_signal = Signal.HIGH

        return out_signal, self.output

    def __str__(self) -> str:
        return f"{self.id} -> {self.output}"
    
    def __repr__(self) -> str:
        return self.__str__()



class Assignment(Solution):
    def parse_input(self, input: str, is_gold: bool = False) -> dict[str, Module]:
        input += "\nbutton -> broadcaster"
        modules = [Module(m) for m in input.splitlines()]
        modules_dict = {m.id: m for m in modules}
        return 
    
    def silver(self, input: dict[str, Module]) -> int:
        print(input)
        return 0
    
    def gold(self, input: dict[str, Module]) -> int:
        return 0