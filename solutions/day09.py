from collections import deque
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
        parts = data[0].split()
        players = int(parts[0])
        marbles = int(parts[-2])

        circle = deque([])
        scores = [0] * players

        i = 0
        m = 0
        while m <= marbles:
            if m and m % 23 == 0:
                scores[i] += m
                circle.rotate(7)
                scores[i] += circle.popleft()
            else:
                circle.insert(2, m)
                idx = circle.index(m)
                circle.rotate(-idx)
            m += 1
            i = (i + 1) % players
        return max(scores)

    def part2(self, data):
        parts = data[0].split()
        players = int(parts[0])
        marbles = int(parts[-2]) * 100

        circle = deque([])
        scores = [0] * players

        i = 0
        m = 0
        while m <= marbles:
            if m and m % 23 == 0:
                scores[i] += m
                circle.rotate(7)
                scores[i] += circle.popleft()
            else:
                circle.insert(2, m)
                idx = circle.index(m)
                circle.rotate(-idx)
            m += 1
            i = (i + 1) % players
        return max(scores)
