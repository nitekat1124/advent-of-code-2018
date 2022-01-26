from collections import defaultdict
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
        grid = defaultdict(int)
        for line in data:
            at_idx = line.index("@")
            pos, dim = line[at_idx + 2 :].split(": ")
            pos = tuple(map(int, pos.split(",")))
            w, h = map(int, dim.split("x"))
            for y in range(h):
                for x in range(w):
                    grid[(pos[0] + x, pos[1] + y)] += 1
        return sum(1 for v in grid.values() if v > 1)

    def part2(self, data):
        grid = defaultdict(list)
        for line in data:
            at_idx = line.index("@")
            id = int(line[1 : at_idx - 1])
            pos, dim = line[at_idx + 2 :].split(": ")
            pos = tuple(map(int, pos.split(",")))
            w, h = map(int, dim.split("x"))
            for y in range(h):
                for x in range(w):
                    grid[(pos[0] + x, pos[1] + y)] += [id]

        grid_values = list(grid.values())
        for id in range(1, len(data) + 1):
            if max([len(v) for v in grid_values if id in v]) == 1:
                return id
