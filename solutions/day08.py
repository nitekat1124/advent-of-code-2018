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
        f = [*map(int, data[0].split())]
        node, _ = self.parse_node(f)
        return node["accu_meta"]

    def part2(self, data):
        f = [*map(int, data[0].split())]
        node, _ = self.parse_node(f)
        return node["value"]

    def parse_node(self, f):
        node = {
            "header": {"child": f[0], "meta": f[1]},
            "child_nodes": [],
            "metadata": [],
            "accu_meta": 0,
            "value": 0,
        }
        f = f[2:]

        for _ in range(node["header"]["child"]):
            child, f = self.parse_node(f)
            node["child_nodes"] += [child]

        node["metadata"] = f[: node["header"]["meta"]]
        node["accu_meta"] = sum(node["metadata"]) + sum(child["accu_meta"] for child in node["child_nodes"])

        node["value"] = sum(node["child_nodes"][i - 1]["value"] for i in node["metadata"] if i <= node["header"]["child"]) if node["header"]["child"] else sum(node["metadata"])

        f = f[node["header"]["meta"] :]

        return node, f
