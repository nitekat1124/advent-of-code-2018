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
        constellations = []
        for line in data:
            point = tuple([int(x) for x in line.strip().split(",")])
            if len(constellations) == 0:
                constellations += [[point]]
            else:
                intersect_group = []
                for i, constellation in enumerate(constellations):
                    if self.is_in_constellation(point, constellation):
                        intersect_group += [i]

                if len(intersect_group) == 0:
                    constellations += [[point]]
                else:
                    new_constellation = [point]
                    for i in intersect_group:
                        new_constellation.extend(constellations[i])
                    for i in sorted(intersect_group)[::-1]:
                        del constellations[i]
                    constellations += [new_constellation]

        return len(constellations)

    def part2(self, data):
        return "Merry Christmas!"

    def is_in_constellation(self, point, constellation):
        for p in constellation:
            if sum(abs(i - j) for i, j in zip(p, point)) <= 3:
                return True
        return False
