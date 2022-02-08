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
        distances = self.get_distances(data[0])
        return max(distances.values())

    def part2(self, data):
        distances = self.get_distances(data[0])
        return sum(1 for i in distances.values() if i >= 1000)

    def get_distances(self, data):
        distances = {}
        positions = []
        x, y = 0, 0
        directions = {"N": (0, -1), "E": (1, 0), "W": (-1, 0), "S": (0, 1)}

        for i in data[1:-1]:
            if i in "NEWS":
                nx, ny = (a + b for a, b in zip(directions[i], (x, y)))
                distance = distances.get((x, y), 0) + 1
                distances[(nx, ny)] = min(distances.get((nx, ny), distance), distance)
                x, y = nx, ny
            elif i == "(":
                positions += [(x, y)]
            elif i == ")":
                positions.pop()
            elif i == "|":
                x, y = positions[-1]

        return distances
