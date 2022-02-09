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
        bots = sorted(self.parse_bots(data), key=lambda x: x[1])[::-1]
        return sum(1 for b in bots if sum(abs(b[0][i] - bots[0][0][i]) for i in range(3)) <= bots[0][1])

    def part2(self, data):
        """
        works for some(my) puzzle input but some others are wrong
        ahhhhhhh need to check later
        check the distance range of every bots and then finds the intersection
        but weird things happen, something must be wrong
        """
        bots = self.parse_bots(data)

        distances = []
        for b in bots:
            d = sum(abs(i) for i in b[0])
            distances.extend([max(0, d - b[1]), d + b[1]])
        distances = [i for i in distances if i > 0]

        c = Counter(distances)

        # return c.most_common(1)[0][0] # it's wrong, but why?
        return max([i[0] for i in c.items() if i[1] > 1])

    def parse_bots(self, data):
        bots = []
        for line in data:
            parts = line.split(">, r=")
            r = int(parts[1])
            coord = tuple(map(int, parts[0].split("<")[1].split(",")))
            bots += [(coord, r)]
        return bots
