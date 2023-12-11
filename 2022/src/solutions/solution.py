from abc import ABC, abstractmethod
from typing import TypeVar, Any
import time
import copy

T = TypeVar('T')
R = TypeVar('R')

class Solution(ABC):
    @abstractmethod
    def parse_input(self) -> T:
        pass
    
    @abstractmethod
    def silver(self, input: T) -> R:
        pass
    
    def timed_silver(self, input: T) -> R:
        start_time = time.time()
        solution = self.silver(input)
        return (solution, time.time() - start_time)
    
    @abstractmethod
    def gold(self, input: T) -> R:
        pass
    
    def timed_gold(self, input: T) -> R:
        start_time = time.time()
        solution = self.gold(input)
        return (solution, time.time() - start_time)
    
    def solve(self, input: str) -> (R, R):
        parsed_input = self.parse_input(input)
        silver_solution, silver_time = self.timed_silver(copy.deepcopy(parsed_input))
        gold_solution, gold_time = self.timed_gold(copy.deepcopy(parsed_input))
        
        print(f"----------\n| Silver | {silver_solution} ({silver_time * 1000000} µs)\n----------\n| Gold   | {gold_solution} ({gold_time * 1000000} µs)\n----------\n")
        
        return (silver_solution, gold_solution)
    