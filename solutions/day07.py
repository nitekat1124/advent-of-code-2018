from collections import defaultdict
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

    def part1_old(self, data):
        steps = defaultdict(list)
        requirements = defaultdict(list)
        for line in data:
            parts = line.split()
            steps[parts[1]] += [parts[7]]
            requirements[parts[7]] += [parts[1]]

        start = sorted([i for i in steps.keys() if i not in requirements.keys()])
        end = [i for i in requirements.keys() if i not in steps.keys()][0]

        insts = []
        queue = start
        waits = []

        while queue:
            queue = sorted(queue)
            inst = queue.pop(0)

            if inst == end:
                break

            insts += [inst]

            for i in sorted(steps[inst])[::-1]:
                if all([x in insts + [inst] for x in requirements[i]]):
                    queue += [i]
                else:
                    if i not in waits and i != end:
                        waits += [i]

            if waits:
                remove_from_waits = []
                for i in waits:
                    if i in insts or i in queue:
                        remove_from_waits += [i]
                    elif all([x in insts + [inst] for x in requirements[i]]):
                        queue += [i]
                        remove_from_waits += [i]

                if remove_from_waits:
                    for i in remove_from_waits:
                        waits.remove(i)

        insts += [end]
        return "".join(insts)

    def part1(self, data):
        requirements = defaultdict(set)
        all_steps = set()

        for line in data:
            parts = line.split()
            all_steps.add(parts[1])
            all_steps.add(parts[7])
            requirements[parts[7]].add(parts[1])

        queue = sorted(all_steps)
        insts = []
        while queue:
            for s in queue:
                if all(x in insts for x in requirements[s]):
                    queue.remove(s)
                    insts += [s]
                    break
        return "".join(insts)

    def part2(self, data):
        requirements = defaultdict(set)
        all_steps = set()

        for line in data:
            parts = line.split()
            all_steps.add(parts[1])
            all_steps.add(parts[7])
            requirements[parts[7]].add(parts[1])

        queue = sorted(all_steps)
        workers = [0, 0] if len(data) == 7 else [0, 0, 0, 0, 0]
        done = defaultdict(int)
        cur_time = 0

        while queue:
            for s in queue:
                if all(0 < done[d] <= cur_time for d in requirements[s]):
                    for wi, wt in enumerate(workers):
                        if wt <= cur_time:
                            workers[wi] = done[s] = cur_time + ord(s) - (64 if len(data) == 7 else 4)
                            break
                    if done[s] > 0:
                        queue.remove(s)
                        break
            else:
                cur_time += 1

        return max(workers)
