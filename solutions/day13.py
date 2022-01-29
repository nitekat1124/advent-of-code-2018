from collections import Counter
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

    def check_is_raw(self):
        if self.is_raw is False:
            print("please use --raw flag in this puzzle")
            exit()

    def part1(self, data):
        self.check_is_raw()

        _map = []
        carts = []
        to = ((0, -1), (1, 0), (0, 1), (-1, 0))

        for y, line in enumerate(data):
            row = ""
            for x, v in enumerate(line):
                if v in "^>v<":
                    d = "^>v<".index(v)
                    carts += [{"pos": (x, y), "dir": d, "trn": 0}]
                    v = "-" if d % 2 else "|"
                row += v
            _map += [row]

        while 1:
            carts = sorted(carts, key=lambda c: (c["pos"][1], c["pos"][0]))
            for idx, cart in enumerate(carts):
                pos = cart["pos"]
                dir = cart["dir"]
                next_pos = (pos[0] + to[dir][0], pos[1] + to[dir][1])
                if _map[next_pos[1]][next_pos[0]] == "+":
                    if cart["trn"] % 3 == 0:
                        carts[idx]["dir"] = (dir + 3) % 4
                    elif cart["trn"] % 3 == 2:
                        carts[idx]["dir"] = (dir + 1) % 4
                    carts[idx]["trn"] += 1
                elif _map[next_pos[1]][next_pos[0]] == "\\":
                    carts[idx]["dir"] = [3, 2, 1, 0][dir]
                elif _map[next_pos[1]][next_pos[0]] == "/":
                    carts[idx]["dir"] = [1, 0, 3, 2][dir]

                carts[idx]["pos"] = next_pos

                res = self.calc_collision(carts)
                if res:
                    return f"{res[0][0]},{res[0][1]}"

    def part2(self, data):
        self.check_is_raw()

        _map = []
        carts = []
        to = ((0, -1), (1, 0), (0, 1), (-1, 0))

        for y, line in enumerate(data):
            row = ""
            for x, v in enumerate(line):
                if v in "^>v<":
                    d = "^>v<".index(v)
                    carts += [{"pos": (x, y), "dir": d, "trn": 0}]
                    v = "-" if d % 2 else "|"
                row += v
            _map += [row]

        while 1:
            if len(carts) == 1:
                return f"{carts[0]['pos'][0]},{carts[0]['pos'][1]}"

            carts = sorted(carts, key=lambda c: (c["pos"][1], c["pos"][0]))
            pop_idx = set()
            for idx, cart in enumerate(carts):
                pos = cart["pos"]
                dir = cart["dir"]
                next_pos = (pos[0] + to[dir][0], pos[1] + to[dir][1])
                if _map[next_pos[1]][next_pos[0]] == "+":
                    if cart["trn"] % 3 == 0:
                        carts[idx]["dir"] = (dir + 3) % 4
                    elif cart["trn"] % 3 == 2:
                        carts[idx]["dir"] = (dir + 1) % 4
                    carts[idx]["trn"] += 1
                elif _map[next_pos[1]][next_pos[0]] == "\\":
                    carts[idx]["dir"] = [3, 2, 1, 0][dir]
                elif _map[next_pos[1]][next_pos[0]] == "/":
                    carts[idx]["dir"] = [1, 0, 3, 2][dir]

                carts[idx]["pos"] = next_pos

                res = self.calc_collision(carts)
                if res:
                    for pos in res:
                        ids = set([i for i, c in enumerate(carts) if c["pos"] == pos])
                        pop_idx |= ids
            for id in sorted(pop_idx)[::-1]:
                del carts[id]

    def calc_collision(self, carts):
        pos = [c["pos"] for c in carts]
        cpos = [c[0] for c in Counter(pos).items() if c[1] > 1]
        if len(cpos) > 0:
            return list(cpos)
        else:
            return False
