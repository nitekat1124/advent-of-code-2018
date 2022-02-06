from collections import deque
from copy import deepcopy
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
        self.parse_data(data)
        self.rounds = 0

        while 1:
            self.sort_units()
            for unit in self.units:
                if len(set(u["type"] for u in self.units if u["hp"] > 0)) == 1:
                    return self.calc_outcome()

                if unit["hp"] <= 0:
                    continue

                adjecent_targets = self.find_adjecents(unit)

                if len(adjecent_targets) == 0:
                    is_moved = self.move_to_nearest_enemy(unit)
                    if is_moved:
                        adjecent_targets = self.find_adjecents(unit)

                if len(adjecent_targets):
                    self.attack(unit, adjecent_targets)

            self.rounds += 1

    def part2(self, data):
        elf_attack = 4

        while 1:
            self.parse_data(data, elf_attack)
            self.rounds = 0

            elf_count = sum(1 for u in self.units if u["type"] == "E")
            res = self.play(elf_count)

            if res:
                survive_type = list(set(u["type"] for u in self.units if u["hp"] > 0))[0]
                survive_count = sum(1 for u in self.units if u["hp"] > 0 and u["type"] == "E")
                if survive_type == "E" and elf_count == survive_count:
                    return self.calc_outcome()

            elf_attack += 1

    def play(self, elf_count):
        while 1:
            self.sort_units()
            for unit in self.units:
                if sum(1 for u in self.units if u["hp"] > 0 and u["type"] == "E") < elf_count:
                    return False
                elif len(set(u["type"] for u in self.units if u["hp"] > 0)) == 1:
                    return True

                if unit["hp"] <= 0:
                    continue

                adjecent_targets = self.find_adjecents(unit)

                if len(adjecent_targets) < 1:
                    m = self.move_to_nearest_enemy(unit)
                    if m:
                        adjecent_targets = self.find_adjecents(unit)

                if len(adjecent_targets):
                    self.attack(unit, adjecent_targets)

            self.rounds += 1

    def parse_data(self, data, elf_attack=3):
        self.map = []
        self.units = []

        for y, line in enumerate(data):
            row = list(line)
            for x, c in enumerate(row):
                if c in "GE":
                    self.units += [{"pos": (x, y), "type": c, "hp": 200, "attack": [elf_attack, 3][c == "G"], "id": len(self.units)}]
                    row[x] = "."
            self.map += [row]

    def sort_units(self):
        self.remove_dead_units()
        self.units.sort(key=lambda u: (u["pos"][1], u["pos"][0]))

    def remove_dead_units(self):
        self.units = [u for u in self.units if u["hp"] > 0]

    def calc_outcome(self):
        self.remove_dead_units()
        return self.rounds * sum([u["hp"] for u in self.units])

    def find_adjecents(self, unit):
        directions = [(0, -1), (-1, 0), (1, 0), (0, 1)]
        adjecents = [(unit["pos"][0] + x, unit["pos"][1] + y) for x, y in directions]
        adjecent_targets = [u["id"] for u in self.units if u["pos"] in adjecents and u["type"] != unit["type"] and u["hp"] > 0]
        return adjecent_targets

    def attack(self, unit, candidates):
        targets = [u for u in self.units if u["id"] in candidates]
        targets.sort(key=lambda u: (u["hp"], u["pos"][1], u["pos"][0]))
        target = targets[0]
        idx = [i for i, u in enumerate(self.units) if u["id"] == target["id"]][0]
        self.units[idx]["hp"] -= unit["attack"]

    def move_to_nearest_enemy(self, unit):
        reachable = self.find_reachable(unit)
        targets = [u for u in self.units if u["type"] != unit["type"] and u["hp"] > 0 and u["pos"] in reachable]
        distances = [(t["id"], t["pos"], reachable[t["pos"]]) for t in targets]

        if len(distances):
            distances.sort(key=lambda t: (len(t[2]), t[1][1], t[1][0]))
            unit["pos"] = distances[0][2][0]
            return True
        else:
            return False

    def find_reachable(self, unit):
        temp_map = self.build_recent_map()
        reachable = {}
        visited = set()
        start = unit["pos"]
        queue = deque([(start, [])])
        while queue:
            pos, path = queue.popleft()
            if pos in visited:
                continue
            visited.add(pos)
            if temp_map[pos[1]][pos[0]] not in ["#", unit["type"]]:
                reachable[pos] = path
            if temp_map[pos[1]][pos[0]] == "." or pos == start:
                for x, y in [(pos[0] + x, pos[1] + y) for x, y in [(0, -1), (-1, 0), (1, 0), (0, 1)]]:
                    if (x, y) not in visited and temp_map[y][x] not in ["#", unit["type"]]:
                        queue.append(((x, y), deepcopy(path) + [(x, y)]))
        return reachable

    def build_recent_map(self):
        map = deepcopy(self.map)
        for u in self.units:
            if u["hp"] > 0:
                map[u["pos"][1]][u["pos"][0]] = u["type"]
        return map
