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
        polymer = [*map(ord, data[0])]
        return self.reacting(polymer)

    def part2(self, data):
        units = set(i for i in data[0] if i.isupper())
        polymers_len = []
        for u in units:
            polymer = [*map(ord, data[0].replace(u, "").replace(u.lower(), ""))]
            polymers_len += [self.reacting(polymer)]
        return min(polymers_len)

    def reacting(self, polymer):
        i = 0
        while i < len(polymer) - 1:
            if abs(polymer[i] - polymer[i + 1]) == 32:
                del polymer[i : i + 2]
                i = max(i - 1, 0)
            else:
                i += 1
        return len(polymer)
