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
        recipes = [3, 7]
        e0 = 0
        e1 = 1
        needed = int(data[0])

        while len(recipes) < needed + 10:
            r0 = recipes[e0]
            r1 = recipes[e1]
            r = r0 + r1
            if r > 9:
                recipes += [1, r - 10]
            else:
                recipes += [r]
            e0 = (e0 + r0 + 1) % len(recipes)
            e1 = (e1 + r1 + 1) % len(recipes)

        scores = recipes[needed : needed + 10]
        return "".join(map(str, scores))

    def part2(self, data):
        recipes = [3, 7]
        e0 = 0
        e1 = 1
        needed = data[0]
        needed_leng = len(needed)

        while 1:
            r0 = recipes[e0]
            r1 = recipes[e1]
            r = r0 + r1
            if r > 9:
                recipes += [1, r - 10]
            else:
                recipes += [r]

            recipes_leng = len(recipes)
            e0 = (e0 + r0 + 1) % recipes_leng
            e1 = (e1 + r1 + 1) % recipes_leng

            if recipes_leng >= needed_leng:
                checking = "".join(map(str, recipes[-needed_leng - 1 :]))
                if checking[:-1] == needed:
                    return recipes_leng - needed_leng - 1
                elif checking[1:] == needed:
                    return recipes_leng - needed_leng
