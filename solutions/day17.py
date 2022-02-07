from collections import defaultdict
from typing import Tuple
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

    def part1_hand_draw(self, data):
        scans = self.parse_data(data)

        # self.render(scans)
        # print()
        # exit()

        y_min = min([*map(lambda x: x[1], scans.keys())])

        with open("data/day17/puzzle_input_rendered.txt", "r") as f:
            content = "".join(f.readlines()[y_min:])
            return content.count("|") + content.count("~")

    def part2_hand_draw(self, data):
        scans = self.parse_data(data)
        y_min = min([*map(lambda x: x[1], scans.keys())])

        with open("data/day17/puzzle_input_rendered.txt", "r") as f:
            content = "".join(f.readlines()[y_min:])
            return content.count("~")

    def part1(self, data):
        self.scans = self.parse_data(data)
        self.ranges = self.get_ranges(self.scans)

        start = (500, 0)
        self.queue = [start]
        while self.queue:
            x, y = self.queue.pop()
            if self.scans[(x, y)] == "~":
                continue
            y += 1
            while y <= self.ranges["y"][1]:
                if self.scans[(x, y)] == ".":
                    self.scans[(x, y)] = "|"
                    y += 1
                elif self.scans[(x, y)] in "#~":
                    y -= 1

                    left_bound, right_bound, is_still = self.check_boundaries(x, y)
                    for xi in range(left_bound, right_bound + 1):
                        self.scans[(xi, y)] = "~" if is_still else "|"
                elif self.scans[(x, y)] == "|":
                    break

        v = [v for k, v in self.scans.items() if k[1] >= self.ranges["y"][0]]
        return v.count("~") + v.count("|")

    def part2(self, data):
        self.scans = self.parse_data(data)
        self.ranges = self.get_ranges(self.scans)

        start = (500, 0)
        self.queue = [start]
        while self.queue:
            x, y = self.queue.pop()
            if self.scans[(x, y)] == "~":
                continue
            y += 1
            while y <= self.ranges["y"][1]:
                if self.scans[(x, y)] == ".":
                    self.scans[(x, y)] = "|"
                    y += 1
                elif self.scans[(x, y)] in "#~":
                    y -= 1

                    left_bound, right_bound, is_still = self.check_boundaries(x, y)
                    for i in range(left_bound, right_bound + 1):
                        self.scans[(i, y)] = "|~"[is_still]
                elif self.scans[(x, y)] == "|":
                    break

        v = [v for k, v in self.scans.items() if k[1] >= self.ranges["y"][0]]
        return v.count("~")

    def parse_data(self, data):
        scans = defaultdict(lambda: ".")

        for line in data:
            a, b = line.split(", ")
            if a[0] == "x":
                x = int(a[2:])
                yr = sorted([*map(int, b[2:].split(".."))])
                yr = range(yr[0], yr[1] + 1)
                for y in yr:
                    scans[(x, y)] = "#"
            else:
                y = int(a[2:])
                xr = sorted([*map(int, b[2:].split(".."))])
                xr = range(xr[0], xr[1] + 1)
                for x in xr:
                    scans[(x, y)] = "#"
        return scans

    def get_ranges(self, scans):
        xs = [*map(lambda k: k[0], scans.keys())]
        ys = [*map(lambda k: k[1], scans.keys())]
        return {"x": (min(xs) - 1, max(xs) + 1), "y": (min(ys), max(ys))}

    def render(self, scans):
        ranges = self.get_ranges(scans)
        render = []
        for y in range(0, ranges["y"][1] + 1):
            row = []
            for x in range(ranges["x"][0], ranges["x"][1] + 1):  # expand 2 sides
                if (x, y) == (500, 0):
                    row += ["+"]
                else:
                    row += [scans[(x, y)]]
            render += [row]
        for row in render:
            print("".join(row))

    def check_boundaries(self, x, y) -> Tuple[int, int, bool]:
        left_bound = None
        right_bound = None
        left_has_wall = False
        right_has_wall = False

        # detect left side boundary
        nearest_left_clay = "".join(self.scans[(i, y)] for i in range(self.ranges["x"][0], x + 1)).rfind("#")
        if nearest_left_clay > -1:
            nearest_left_clay += self.ranges["x"][0]

        nearest_left_bottom_sand = "".join(self.scans[(i, y + 1)] for i in range(self.ranges["x"][0], x + 1)).rfind(".")
        if nearest_left_bottom_sand > -1:
            nearest_left_bottom_sand += self.ranges["x"][0]

        if nearest_left_clay > -1 and nearest_left_clay >= nearest_left_bottom_sand:
            left_bound = nearest_left_clay + 1
            left_has_wall = True
        elif nearest_left_bottom_sand > nearest_left_clay:
            left_bound = nearest_left_bottom_sand
            self.queue += [(nearest_left_bottom_sand, y)]

        # detect right side boundary
        nearest_right_clay = "".join(self.scans[(i, y)] for i in range(x, self.ranges["x"][1] + 1)).find("#")
        if nearest_right_clay > -1:
            nearest_right_clay += x
        else:
            nearest_right_clay = self.ranges["x"][1] + 1

        nearest_right_bottom_sand = "".join(self.scans[(i, y + 1)] for i in range(x, self.ranges["x"][1] + 1)).find(".")
        if nearest_right_bottom_sand > -1:
            nearest_right_bottom_sand += x
        else:
            nearest_right_bottom_sand = self.ranges["x"][1] + 1

        if nearest_right_clay > -1 and nearest_right_clay <= nearest_right_bottom_sand:
            right_bound = nearest_right_clay - 1
            right_has_wall = True
        elif nearest_right_bottom_sand < nearest_right_clay:
            right_bound = nearest_right_bottom_sand
            self.queue += [(nearest_right_bottom_sand, y)]

        return (left_bound, right_bound, left_has_wall and right_has_wall)
