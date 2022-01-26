from collections import Counter
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
        c2 = 0
        c3 = 0
        for i in data:
            c = Counter(i)
            if 2 in c.values():
                c2 += 1
            if 3 in c.values():
                c3 += 1

        return c2 * c3

    def part2(self, data):
        for i, id in enumerate(data):
            for id2 in data[i + 1 :]:
                same = []
                for c1, c2 in zip(id, id2):
                    if c1 == c2:
                        same += [c1]
                if len(same) == len(id) - 1:
                    return "".join(same)
