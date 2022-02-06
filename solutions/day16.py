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
        samples, insts = "\n".join(data).split("\n\n\n\n")
        samples = [i.split("\n") for i in samples.split("\n\n")]

        opcode_mapper = self.get_opcode_mapper(samples)
        return len([1 for o in opcode_mapper if len(o[2]) > 2])

    def part2(self, data):
        samples, insts = "\n".join(data).split("\n\n\n\n")
        samples = [i.split("\n") for i in samples.split("\n\n")]
        insts = [i for i in insts.split("\n")]

        opcode_mapper = self.get_opcode_mapper(samples)
        opcodes = self.resolve_opcodes(opcode_mapper)
        regs = self.run_insts([0, 0, 0, 0], insts, opcodes)
        return regs[0]

    def get_opcode_mapper(self, data):
        opcodes = ["addr", "addi", "mulr", "muli", "banr", "bani", "borr", "bori", "setr", "seti", "gtir", "gtri", "gtrr", "eqir", "eqri", "eqrr"]
        opcode_mapper = []

        for i, sample in enumerate(data):
            bef = sample[0][9:-1]
            aft = sample[2][9:-1]
            op = [*map(int, sample[1].split(" "))]

            matched_opcodes = set()
            for o in opcodes:
                test = self.run_inst(bef, o, op[1:])
                if aft == test:
                    matched_opcodes.add(o)
            opcode_mapper += [(i, op[0], matched_opcodes)]
        return opcode_mapper

    def resolve_opcodes(self, opcode_mapper):
        opcodes = {}
        resorts = {}

        for _, opcode, matches in opcode_mapper:
            if opcode in resorts:
                resorts[opcode] &= matches
            else:
                resorts[opcode] = matches

        while len(resorts):
            for opcode in resorts:
                if len(resorts[opcode]) == 1:
                    opcodes[opcode] = list(resorts[opcode])[0]

            resorts = {k: v for k, v in resorts.items() if len(v) > 1}

            confirmed = set(opcodes.values())

            for opcode in resorts:
                resorts[opcode] -= confirmed

        return opcodes

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

    def run_insts(self, regs, insts, opcodes):
        for inst in insts:
            opcode, *io = [*map(int, inst.split(" "))]
            regs = self.run_inst(regs, opcodes[opcode], io, False)
        return regs
