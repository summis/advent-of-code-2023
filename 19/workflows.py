with open("input") as f:
    [flows, inputs] = f.read().split("\n\n")


def parse_inputs(inputs):
    parsed = []
    for _input in inputs.splitlines():
        element = {}
        for rating in _input[1:-1].split(","):
            [category, _value] = rating.split("=")
            element[category] = int(_value)
        parsed.append(element)
    return parsed


def parse_flows(flows):
    parsed = {}
    for _flow in flows.splitlines():
        [id, rules] = _flow.replace("}", "").split("{")
        for i, rule in enumerate(rules.split(",")):
            parsed[id if i == 0 else id + str(i)] = parse_rule(rule, id + str(i + 1))
    return parsed


def parse_rule(rule, false_target):
    if rule in ("A", "R"):
        return {"f": lambda e: rule == "A", True: "A", False: "R"}
    elif "<" in rule:
        [c, value, target] = rule.replace(":", "<").split("<")
        return {"f": lambda e: e[c] < int(value), True: target, False: false_target}
    elif ">" in rule:
        [c, value, target] = rule.replace(":", ">").split(">")
        return {"f": lambda e: e[c] > int(value), True: target, False: false_target}
    else:
        return {
            "f": lambda e: True,
            True: rule,
        }


def part1():
    parts = parse_inputs(inputs)
    tree = parse_flows(flows)
    handled = {"A": [], "R": []}

    for part in parts:
        root = "in"
        while root not in ("A", "R"):
            leaf = tree[root]["f"](part)
            root = tree[root][leaf]
        handled[root].append(part)

    return sum(sum(x.values()) for x in handled["A"])


def parse_flows_2(rules):
    parsed = {}
    for _flow in flows.splitlines():
        [id, _rules] = _flow.replace("}", "").split("{")
        parsed[id] = _rules.split(",")

    return parsed


def part2():
    todos = [("in", {"m": (1, 4001), "a": (1, 4001), "s": (1, 4001), "x": (1, 4001)})]
    rules = parse_flows_2(flows)
    handled = {"A": [], "R": []}

    def apply_rule(e, rules):
        rule = rules[0]

        if len(rules) == 1:
            todos.append((rule, e))

        if "<" in rule:
            [c, value, target] = rule.replace(":", "<").split("<")

            r1, r2 = e[c]

            true_range = (r1, min(r2, int(value)))
            if true_range[0] < true_range[1]:
                e1 = e.copy()
                e1[c] = true_range
                todos.append((target, e1))

            false_range = (max(r1, int(value)), r2)
            if false_range[0] < false_range[1]:
                e2 = e.copy()
                e2[c] = false_range
                apply_rule(e2, rules[1:])

        if ">" in rule:
            [c, value, target] = rule.replace(":", ">").split(">")

            r1, r2 = e[c]

            true_range = (max(r1, int(value) + 1), r2)
            if true_range[0] < true_range[1]:
                e1 = e.copy()
                e1[c] = true_range
                todos.append((target, e1))

            false_range = (r1, min(r2, int(value) + 1))
            if false_range[0] < false_range[1]:
                e2 = e.copy()
                e2[c] = false_range
                apply_rule(e2, rules[1:])

    while todos:
        node, e = todos.pop()

        if node in ("A", "R"):
            handled[node].append(e)
            continue

        apply_rule(e, rules[node])

    return sum(
        (x["a"][1] - x["a"][0])
        * (x["s"][1] - x["s"][0])
        * (x["x"][1] - x["x"][0])
        * (x["m"][1] - x["m"][0])
        for x in handled["A"]
    )


print(part1(), part2())
