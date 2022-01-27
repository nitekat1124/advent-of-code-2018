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
        points = [tuple(map(int, line.split(", "))) for line in data]
        areas = [0] * len(points)
        edges = set()

        x_range = range(min(points, key=lambda p: p[0])[0], max(points, key=lambda p: p[0])[0] + 1)
        y_range = range(min(points, key=lambda p: p[1])[1], max(points, key=lambda p: p[1])[1] + 1)

        for y in y_range:
            for x in x_range:
                distances = [abs(x - p[0]) + abs(y - p[1]) for p in points]
                min_distance = min(distances)
                if distances.count(min_distance) == 1:
                    closest_point = distances.index(min_distance)
                    areas[closest_point] += 1
                    if x in [min(x_range), max(x_range)] or y in [min(y_range), max(y_range)]:
                        edges.add(closest_point)

        for p in edges:
            areas[p] = -1

        return max(areas)

    def part2(self, data):
        points = [tuple(map(int, line.split(", "))) for line in data]
        safes = set()
        safe_range = 32 if len(data) == 6 else 10000

        x_range = range(min(points, key=lambda p: p[0])[0], max(points, key=lambda p: p[0])[0] + 1)
        y_range = range(min(points, key=lambda p: p[1])[1], max(points, key=lambda p: p[1])[1] + 1)

        for y in y_range:
            for x in x_range:
                distances = sum([abs(x - p[0]) + abs(y - p[1]) for p in points])
                if distances < safe_range:
                    safes.add((x, y))

        return len(safes)
