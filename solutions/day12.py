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
        gen = 20
        state = list(".." * gen + data[0].split()[2] + ".." * gen)
        notes = {}
        for line in data[2:]:
            parts = line.split(" => ")
            notes[parts[0]] = parts[1]

        for _ in range(gen):
            new_state = ["."] * len(state)
            for i in range(2, len(state) - 2):
                status = "".join(state[i - 2 : i + 3])
                if status in notes:
                    new_state[i] = notes[status]
            state = new_state
        return sum(i - gen * 2 for i, v in enumerate(state) if v == "#")

    def part2(self, data):
        """
        observ the differences between the first 500 generations
        and it will eventually convergence to the same value of the last 100 diff's avarage
        """
        gen = 500
        state = list(".." * gen + data[0].split()[2] + ".." * gen)
        notes = {}
        for line in data[2:]:
            parts = line.split(" => ")
            notes[parts[0]] = parts[1]

        prev_sum = sum(i - gen * 2 for i, v in enumerate(state) if v == "#")
        diffs = []

        for x in range(gen):
            new_state = ["."] * len(state)

            for i in range(2, len(state) - 2):
                status = "".join(state[i - 2 : i + 3])
                if status in notes:
                    new_state[i] = notes[status]
            state = new_state
            this_sum = sum(i - gen * 2 for i, v in enumerate(state) if v == "#")
            diffs += [this_sum - prev_sum]
            prev_sum = this_sum
            diffs = diffs[-100:]
            diff_avg = sum(diffs) // len(diffs)
            # print(x + 1, diff_avg)

        return (50000000000 - gen) * diff_avg + prev_sum
