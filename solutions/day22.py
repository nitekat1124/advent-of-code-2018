import networkx as nx
from utils.solution_base import SolutionBase


class Solution(SolutionBase):
    def solve(self, part_num: int):
        self.test_runner(part_num)

        func = getattr(self, f"part{part_num}")
        result = func(self.data)
        return result

    def test_runner(self, part_num):
        test_inputs = self.get_test_input()
        test_results = self.get_test_result(part_num)
        test_counter = 1

        func = getattr(self, f"part{part_num}")
        for i, r in zip(test_inputs, test_results):
            if len(r):
                if (tr := str(func(i))) == r[0]:
                    print(f"test {test_counter} passed")
                else:
                    print(f"your result: {tr}")
                    print(f"test answer: {r[0]}")
                    print(f"test {test_counter} NOT passed")
            test_counter += 1
        print()

    def part1(self, data):
        depth = int(data[0].split(": ")[1])
        target = tuple(map(int, data[1].split(": ")[1].split(",")))

        types = {}
        self.erosions = {(0, 0): depth % 20183, target: depth % 20183}

        for x in range(target[0] + 1):
            for y in range(target[1] + 1):
                erosion = self.get_erosion(x, y, depth)
                types[(x, y)] = erosion % 3
        return sum(types.values())

    def part2(self, data):
        depth = int(data[0].split(": ")[1])
        target = tuple(map(int, data[1].split(": ")[1].split(",")))

        self.types = {}
        self.erosions = {(0, 0): depth % 20183, target: depth % 20183}

        expand_size = 15

        for x in range(target[0] + expand_size):
            for y in range(target[1] + expand_size):
                erosion = self.get_erosion(x, y, depth)
                self.types[(x, y)] = erosion % 3

        return self.calc_dijkstra(target, expand_size)

    def get_erosion(self, x, y, depth):
        if (x, y) not in self.erosions:
            if x == 0:
                geologic = y * 48271
            elif y == 0:
                geologic = x * 16807
            else:
                geologic = self.get_erosion(x - 1, y, depth) * self.get_erosion(x, y - 1, depth)
            erosion = (geologic + depth) % 20183
            self.erosions[(x, y)] = erosion

        return self.erosions[(x, y)]

    def calc_dijkstra(self, target, expand_size):
        # rocky = 0, wet = 1, narrow = 2
        # neither = 0, torch = 1, climbing = 2

        g = nx.Graph()

        for x in range(target[0] + expand_size):
            for y in range(target[1] + expand_size):
                tools = list({0, 1, 2} - {self.types[(x, y)]})

                g.add_edge(((x, y), tools[0]), ((x, y), tools[1]), time=7)

                for x2, y2 in [(x + dx, y + dy) for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]]:

                    if (x2, y2) in self.types:
                        tools_next = {0, 1, 2} - {self.types[(x2, y2)]}

                        for tool in set(tools) & tools_next:
                            g.add_edge(((x, y), tool), ((x2, y2), tool), time=1)

        return nx.shortest_path_length(g, ((0, 0), 1), (target, 1), weight="time")
