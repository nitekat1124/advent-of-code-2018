from binascii import crc32
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
        _map = self.parse_data(data)
        for _ in range(10):
            _map = self.magic(_map)
        return self.calc_value(_map)

    def part2(self, data):
        _map = self.parse_data(data)
        patterns = [self.hash(_map)]

        check_pattern = True
        times = 1000000000
        i = 0

        while i < times:
            _map = self.magic(_map)
            _hash = self.hash(_map)

            if check_pattern and _hash in patterns:
                prev_idx = patterns.index(_hash)
                curr_idx = len(patterns)
                diff = curr_idx - prev_idx
                left = 1 + (times - prev_idx - 1) % diff
                i = times - left
                check_pattern = False
            else:
                patterns.append(_hash)
                i += 1

        return self.calc_value(_map)

    def hash(self, _map):
        data = "".join(_map[(x, y)] for y in range(50) for x in range(50))
        return crc32(data.encode())

    def parse_data(self, data):
        _map = {}
        for y, line in enumerate(data):
            for x, arce in enumerate(line):
                _map[(x, y)] = arce
        return _map

    def magic(self, _map):
        _next_map = {}
        dirs = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for x, y in _map:
            arce = _map[(x, y)]
            neighbors = [_map[i] for i in [(x + a, y + b) for a, b in dirs] if i in _map]
            if arce == ".":
                _next_map[(x, y)] = ".|"[neighbors.count("|") > 2]
            elif arce == "|":
                _next_map[(x, y)] = "|#"[neighbors.count("#") > 2]
            elif arce == "#":
                _next_map[(x, y)] = ".#"[neighbors.count("#") > 0 and neighbors.count("|") > 0]
        return _next_map

    def calc_value(self, _map):
        data = list(_map.values())
        return data.count("|") * data.count("#")
