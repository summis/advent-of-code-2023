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
            parsed[id if i == 0 else id+str(i)] = parse_rule(rule, id+str(i+1))
    return parsed


def parse_rule(rule, false_target):
    if rule in ("A", "R"):
        return {
            "f": lambda e: rule == "A",
            True: "A",
            False: "R"
        }
    elif "<" in rule:
        [c, value, target] = rule.replace(":", "<").split("<")
        return {
            "f": lambda e: e[c] < int(value),
            True: target,
            False: false_target
        }
    elif ">" in rule:
        [c, value, target] = rule.replace(":", ">").split(">")
        return {
            "f": lambda e: e[c] > int(value),
            True: target,
            False: false_target
        }
    else:
        return {
            "f": lambda e: True,
            True: rule,
        }


def part1():
    parts = parse_inputs(inputs)
    tree = parse_flows(flows)
    handled = {
        "A": [],
        "R": []
    }

    for part in parts:
        root = "in"
        while root not in ("A", "R"):
            leaf = tree[root]["f"](part)
            root = tree[root][leaf]
        handled[root].append(part)

    return sum(sum(x.values()) for x in handled["A"])

print(part1())