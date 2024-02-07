import math
from enum import Enum
from .solution import Solution


class Signal(Enum):
    HIGH = 1
    LOW = 0
    FINISHED = -1

    def __str__(self) -> str:
        return str(f"-{self.name}->")

    def __repr__(self) -> str:
        return self.__str__()


class ModuleType(Enum):
    BUTTON = "button"
    BROADCASTER = "broadcaster"
    FLIP_FLOP = "%"
    CONJUNCTION = "&"
    OUTPUT = "^"


class Module:
    def __init__(self, input: str) -> None:
        input_output = input.split(" -> ")

        self.id = input_output[0]
        self.input = []
        self.output = input_output[1].split(", ")

        if input_output[0] == ModuleType.BUTTON.value:
            self.type = ModuleType.BUTTON
        elif input_output[0] == ModuleType.BROADCASTER.value:
            self.type = ModuleType.BROADCASTER
        else:
            self.id = input_output[0][1:]
            self.type = ModuleType(input_output[0][0])
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
            out_signal = Signal(signal.value)
        elif self.type == ModuleType.FLIP_FLOP:
            if signal == Signal.LOW:
                self.on = not self.on
                out_signal = Signal(self.on)
        elif self.type == ModuleType.CONJUNCTION:
            self.memory[source] = signal
            if all([s.value for s in self.memory.values()]):
                out_signal = Signal.LOW
            else:
                out_signal = Signal.HIGH
        elif self.type == ModuleType.OUTPUT and signal == Signal.LOW:
            out_signal = Signal.FINISHED

        return out_signal, self.output

    def __str__(self) -> str:
        output = f"{self.id} -> {self.output}"
        if self.type == ModuleType.FLIP_FLOP:
            output += f" ({self.on})"
        elif self.type == ModuleType.CONJUNCTION:
            output += f" ({self.memory})"
        return 

    def __repr__(self) -> str:
        return self.__str__()


class Assignment(Solution):
    def parse_input(self, input: str, is_gold: bool = False) -> dict[str, Module]:
        # input += "\nbutton -> broadcaster"
        input += "\n^output -> output"
        input += "\n^rx -> rx"
        modules = [Module(m) for m in input.splitlines()]
        modules_dict = {m.id: m for m in modules}
        for module in modules:
            for output in module.output:
                modules_dict[output].add_input([module.id])
        return modules_dict

    def silver(self, input: dict[str, Module]) -> int:
        # print(input)
        button_pressed = 1000
        signal_count = [0, 0]
        for _ in range(button_pressed):
            signal_backlog = [("button", Signal.LOW, "broadcaster")]
            while len(signal_backlog) > 0:
                source, signal, dest = signal_backlog.pop(0)
                # print(f"{signal} {dest}")
                signal_count[signal.value] += 1
                out_signal, output = input[dest].process_signal(signal, source)
                if out_signal is not None and out_signal != Signal.FINISHED:
                    for o in output:
                        # print(f"{dest} {out_signal} {o}")
                        signal_backlog.append((dest, out_signal, o))
        # print(signal_count)
        return math.prod(signal_count)

    def gold(self, input: dict[str, Module]) -> int:
        if "rx" not in input:
            return 0

        # print(input)
        button_pressed = 0
        # while True:
        while button_pressed < 4:
            button_pressed += 1
            signal_count = [0, 0]

            signal_backlog = [("button", Signal.LOW, "broadcaster")]
            while len(signal_backlog) > 0:
                source, signal, dest = signal_backlog.pop(0)
                print(f"{signal} {dest}")
                signal_count[signal.value] += 1
                out_signal, output = input[dest].process_signal(signal, source)
                if out_signal == Signal.FINISHED:
                    return button_pressed
                if out_signal is not None and out_signal != Signal.FINISHED:
                    for o in output:
                        print(f"{dest} {out_signal} {o}")
                        signal_backlog.append((dest, out_signal, o))
            # print(input["jg"], input["jg"].memory)
            # print(input["rh"], input["rh"].memory)
            # print(input["jm"], input["jm"].memory)
            # print(input["hf"], input["hf"].memory)
            # if signal_count[0] == 9 and signal_count[1] == 35:
            #     continue
            print(f"===== Signal Count {signal_count} ({button_pressed}) =====")
