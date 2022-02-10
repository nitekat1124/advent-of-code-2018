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
        idx = data.index("")
        immunesys = self.parse_groups(data[1:idx])
        infection = self.parse_groups(data[idx + 2 :])

        imm_units, inf_units = self.fight(immunesys, infection)
        return imm_units + inf_units

    def part2(self, data):
        boost = 1
        while 1:
            idx = data.index("")
            immunesys = self.parse_groups(data[1:idx], boost)
            infection = self.parse_groups(data[idx + 2 :])

            result = self.fight(immunesys, infection)
            if result is not False and result[0] > 0 and result[1] == 0:
                return result[0]
            else:
                boost += 1

    def parse_groups(self, data, boost=0):
        groups = []
        gid = 1
        for line in data:
            group = {}
            group["id"] = gid

            idx1 = line.find("(")
            idx2 = line.find(")")
            if idx1 < 0 and idx2 < 0:
                idx3 = line.find("with an attack")
                part1 = line[:idx3]
                part3 = line[idx3:]
                part2 = False
            else:
                part1 = line[:idx1]
                part2 = line[idx1 + 1 : idx2]
                part3 = line[idx2 + 1 :]

            part1 = part1.strip().split()
            group["units"] = int(part1[0])
            group["hp"] = int(part1[4])

            part3 = part3.strip().split()
            group["attack_damage"] = int(part3[5]) + boost
            group["attack_type"] = part3[6]
            group["initiative"] = int(part3[-1])

            group["immune"] = []
            group["weak"] = []

            if part2:
                part2 = part2.strip().split("; ")
                for line2 in part2:
                    part2_sub = line2.split(" ", 2)
                    types = part2_sub[2].split(", ")
                    group[part2_sub[0]] = types

            group["power"] = group["units"] * group["attack_damage"]
            groups += [group]

            gid += 1
        return groups

    def fight(self, immunesys, infection):
        last_fight_result = None
        while 1:
            # infection select order by power and initiative
            infection.sort(key=lambda x: (x["power"], x["initiative"]), reverse=True)

            inf_targets = []
            for inf in infection:
                if inf["units"] <= 0:
                    continue
                attack = inf["attack_damage"] * inf["units"]
                targets = []
                selected = [t[1][0] for t in inf_targets if t[1] is not False]

                for g in immunesys:
                    if g["units"] > 0 and g["id"] not in selected and inf["attack_type"] not in g["immune"]:
                        times = 2 if inf["attack_type"] in g["weak"] else 1
                        targets += [(g["id"], times * attack, g["power"], g["initiative"])]
                if len(targets):
                    targets.sort(key=lambda x: (x[1], x[2], x[3]), reverse=True)
                    inf_targets += [((inf["id"], "inf", inf["initiative"]), targets[0])]
                else:
                    inf_targets += [((inf["id"], "inf", inf["initiative"]), False)]

            # immune select order by power and initiative
            immunesys.sort(key=lambda x: (x["power"], x["initiative"]), reverse=True)

            imm_targets = []
            for imm in immunesys:
                if imm["units"] <= 0:
                    continue
                attack = imm["attack_damage"] * imm["units"]
                targets = []
                selected = [t[1][0] for t in imm_targets if t[1] is not False]

                for g in infection:
                    if g["units"] > 0 and g["id"] not in selected and imm["attack_type"] not in g["immune"]:
                        times = 2 if imm["attack_type"] in g["weak"] else 1
                        targets += [(g["id"], times * attack, g["power"], g["initiative"])]
                if len(targets):
                    targets.sort(key=lambda x: (x[1], x[2], x[3]), reverse=True)
                    imm_targets += [((imm["id"], "imm", imm["initiative"]), targets[0])]
                else:
                    imm_targets += [((imm["id"], "imm", imm["initiative"]), False)]

            # attack by order of initiative
            all_groups = sorted(inf_targets + imm_targets, key=lambda x: x[0][2], reverse=True)
            for g in all_groups:
                if g[1] is not False:
                    attacker = [gr for gr in [immunesys, infection][g[0][1] == "inf"] if gr["id"] == g[0][0]][0]
                    defender = [gr for gr in [infection, immunesys][g[0][1] == "inf"] if gr["id"] == g[1][0]][0]
                    attack_damage = attacker["attack_damage"] * attacker["units"] * (2 if attacker["attack_type"] in defender["weak"] else 1)
                    defender["units"] -= attack_damage // defender["hp"]
                    if defender["units"] <= 0:
                        defender["units"] = 0
                    defender["power"] = defender["units"] * defender["attack_damage"]

            imm_units = sum(g["units"] for g in immunesys)
            inf_units = sum(g["units"] for g in infection)
            fight_result = (imm_units, inf_units)

            if 0 in fight_result:
                return fight_result
            elif last_fight_result == fight_result:
                return False
            else:
                last_fight_result = fight_result
