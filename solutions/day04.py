from collections import Counter, defaultdict
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
        data = sorted(data)
        records = sorted(self.parse(data).items(), key=lambda x: len(x[1]), reverse=True)

        for r in records:
            x = Counter(r[1]).most_common(1)
            if x[0][1] > 1:
                return r[0] * x[0][0]

    def part2(self, data):
        data = sorted(data)
        records = sorted(self.parse(data).items(), key=lambda r: Counter(r[1]).most_common(1)[0][1], reverse=True)

        for r in records:
            x = Counter(r[1]).most_common(1)
            if x[0][1] > 1:
                return r[0] * x[0][0]

    def parse(self, data):
        records = defaultdict(list)
        id = None
        sleep = []

        for line in data:
            d, t = line[1:17].split()
            if line[25] == "#":
                id = int(line[26:].split()[0])
                sleep = []
            elif "asleep" in line:
                sleep += [int(t[3:])]
            elif "wakes" in line:
                sleep += [int(t[3:])]
                records[id] += [*range(sleep[0], sleep[1])]
                sleep = []

        return records
