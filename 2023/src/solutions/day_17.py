from .solution import Solution


class Grid:
    def __init__(self, input: str):
        self.grid = [[int(char) for char in line] for line in input.split("\n")]
        self.width = len(self.grid[0])
        self.height = len(self.grid)

    def possible_next(self, coord: tuple[int, int]) -> list[tuple[int, int]]:
        x, y = coord
        possible = []
        if x > 0:
            possible.append(((x - 1, y), 'w'))
        if x < self.width - 1:
            possible.append(((x + 1, y), 'e'))
        if y > 0:
            possible.append(((x, y - 1), 'n'))
        if y < self.height - 1:
            possible.append(((x, y + 1), 's'))
        return possible

    def dijkstra(self, start: tuple[int, int], end: tuple[int, int]) -> int:
        visited = set()
        distances = dict()
        for y in range(self.height):
            for x in range(self.width):
                distances[(x, y)] = (float("inf"), [])
        distances[start] = (self.grid[start[1]][start[0]], [])
        while len(visited) < self.width * self.height:
            current = None
            # print(distances)
            for coord in distances:
                if coord not in visited and (current is None or distances[coord][0] < distances[current][0]):
                    current = coord
            visited.add(current)
            previous_distance = distances[current][1]
            print(current, previous_distance)
            for (coord, dir) in self.possible_next(current):

                print(coord, dir, (len(previous_distance) < 3 or any([dir != d for d in previous_distance[-3:]])), distances[coord][0] > distances[current][0] + self.grid[coord[1]][coord[0]], coord in visited)
                if len(previous_distance) < 3 or any([dir != d for d in previous_distance[-3:]]):
                    if distances[coord][0] > distances[current][0] + self.grid[coord[1]][coord[0]]:
                        distances[coord] = (min(distances[coord][0], distances[current][0] + self.grid[coord[1]][coord[0]]), previous_distance + [dir])
                        if coord in visited:
                            visited.remove(coord)
            print(distances)
        return distances[end]
        

    def __str__(self) -> str:
        return "\n".join(["".join([str(char) for char in line]) for line in self.grid])
    
    def __repr__(self) -> str:
        return self.__str__()



class Assignment(Solution):
    def parse_input(self, input: str, is_gold: bool = False) -> Grid:
        return Grid(input)
    
    def silver(self, input: Grid) -> int:
        print(input)
        return input.dijkstra((0, 0), (input.width - 1, input.height - 1))
        return 0
    
    def gold(self, input: Grid) -> int:
        return 0