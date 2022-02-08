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
        regs = [0] * 6
        ip = int(data[0].split(" ")[1])
        i = regs[ip]

        while 1:
            if i == 29:
                return regs[4]

            inst, *io = data[i + 1].split(" ")
            io = [*map(int, io)]
            regs = self.run_inst(regs, inst, io, False)

            if regs[ip] + 1 < len(data) - 1:
                regs[ip] += 1
                i = regs[ip]
            else:
                break

    def part2(self, data):
        """
        super slow, might optimize later, have no idea how for now
        """
        regs = [0] * 6
        ip = int(data[0].split(" ")[1])
        i = regs[ip]

        detected = set()
        prev = 0

        while 1:
            if i == 29:
                if regs[4] in detected:
                    return prev
                prev = regs[4]
                detected.add(regs[4])

            inst, *io = data[i + 1].split(" ")
            io = [*map(int, io)]
            regs = self.run_inst(regs, inst, io, False)

            if regs[ip] + 1 < len(data) - 1:
                regs[ip] += 1
                i = regs[ip]
            else:
                break

    def run_inst(self, regs, opcode, io, as_str=True):
        if as_str:
            regs = [*map(int, regs.split(", "))]

        if opcode == "addr":
            regs[io[2]] = regs[io[0]] + regs[io[1]]
        elif opcode == "addi":
            regs[io[2]] = regs[io[0]] + io[1]
        elif opcode == "mulr":
            regs[io[2]] = regs[io[0]] * regs[io[1]]
        elif opcode == "muli":
            regs[io[2]] = regs[io[0]] * io[1]
        elif opcode == "banr":
            regs[io[2]] = regs[io[0]] & regs[io[1]]
        elif opcode == "bani":
            regs[io[2]] = regs[io[0]] & io[1]
        elif opcode == "borr":
            regs[io[2]] = regs[io[0]] | regs[io[1]]
        elif opcode == "bori":
            regs[io[2]] = regs[io[0]] | io[1]
        elif opcode == "setr":
            regs[io[2]] = regs[io[0]]
        elif opcode == "seti":
            regs[io[2]] = io[0]
        elif opcode == "gtir":
            regs[io[2]] = int(io[0] > regs[io[1]])
        elif opcode == "gtri":
            regs[io[2]] = int(regs[io[0]] > io[1])
        elif opcode == "gtrr":
            regs[io[2]] = int(regs[io[0]] > regs[io[1]])
        elif opcode == "eqir":
            regs[io[2]] = int(io[0] == regs[io[1]])
        elif opcode == "eqri":
            regs[io[2]] = int(regs[io[0]] == io[1])
        elif opcode == "eqrr":
            regs[io[2]] = int(regs[io[0]] == regs[io[1]])

        return ", ".join(str(r) for r in regs) if as_str else regs
