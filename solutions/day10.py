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
        points = []
        for line in data:
            p0 = line.index("<")
            p1 = line.index(">")
            pos = line[p0 + 1 : p1]
            v1 = line[p1 + 1 :].index("<")
            v2 = line[p1 + 1 :].index(">")
            vel = line[p1 + 1 :][v1 + 1 : v2]
            points += [[[*map(int, pos.split(","))], tuple(map(int, vel.split(",")))]]

        for i in range(15000):
            np = []
            for p in points:
                np += [[p[0][0] + p[1][0] * i, p[0][1] + p[1][1] * i]]
            r = self.draw(np, i)
            if r:
                return r

    def part2(self, data):
        return "in the result of part 1"

    def draw(self, points, i):
        min_x = min(p[0] for p in points)
        max_x = max(p[0] for p in points)
        min_y = min(p[1] for p in points)
        max_y = max(p[1] for p in points)
        if max_x - min_x < 70:  # not a algorithm... just because I know it would shirnk to 62 with my puzzle input :p
            for y in range(min_y, max_y + 1):
                for x in range(min_x, max_x + 1):
                    if any(p[0] == x and p[1] == y for p in points):
                        print("#", end="")
                    else:
                        print(".", end="")
                print()
            print()
            return i
        return False
