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
        serial = int(data[0])
        w = 300
        h = 300
        grid = []

        for y in range(1, h + 1):
            g = []
            for x in range(1, w + 1):
                rack_id = x + 10
                power = (((rack_id * y + serial) * rack_id) // 100) % 10 - 5
                g += [power]
            grid += [g]

        power = []
        for i in range(0, w - 2):
            for j in range(0, h - 2):
                p = sum(sum(g[i : i + 3]) for g in grid[j : j + 3])
                power += [(p, (i + 1, j + 1))]
        p = max(power)[1]

        return f"{p[0]},{p[1]}"

    def part2_org(self, data):
        serial = int(data[0])
        w = 300
        h = 300
        grid = []

        for y in range(1, h + 1):
            g = []
            for x in range(1, w + 1):
                rack_id = x + 10
                power = (((rack_id * y + serial) * rack_id) // 100) % 10 - 5
                g += [power]
            grid += [g]

        power = []
        for size in range(1, w + 1):
            # print(size)
            for i in range(0, w - size + 1):
                for j in range(0, h - size + 1):
                    p = sum(sum(g[i : i + size]) for g in grid[j : j + size])
                    power += [(p, (i + 1, j + 1), size)]
        p = max(power)

        return f"{p[1][0]},{p[1][1]},{p[2]}"

    def part2(self, data):
        serial = int(data[0])
        w = 300
        h = 300
        grid = []

        for y in range(1, h + 1):
            g = []
            for x in range(1, w + 1):
                rack_id = x + 10
                power = (((rack_id * y + serial) * rack_id) // 100) % 10 - 5
                g += [power]
            grid += [g]

        # building summed area table
        # ref: https://www.geeksforgeeks.org/submatrix-sum-queries/
        summed_table = defaultdict(int)
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                summed_table[(x, y)] = sum(sum(grid[j][: x + 1]) for j in range(y + 1))

        power = []
        for size in range(1, w + 1):
            # print(size)
            for i in range(0, w - size + 1):
                for j in range(0, h - size + 1):
                    # p = sum(sum(g[i : i + size]) for g in grid[j : j + size])
                    p = summed_table[(i + size - 1, j + size - 1)] - summed_table[(i - 1, j + size - 1)] - summed_table[(i + size - 1, j - 1)] + summed_table[(i - 1, j - 1)]
                    power += [(p, (i + 1, j + 1), size)]
        p = max(power)

        return f"{p[1][0]},{p[1][1]},{p[2]}"
