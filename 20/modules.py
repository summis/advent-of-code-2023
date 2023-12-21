with open("input") as f:
    data = f.read().splitlines()


def parse_circuit(data):
    circuit = {}
    for row in data:
        [id, targets] = row.split(" -> ")
        if "%" in id:
            circuit[id[1:]] = {
                "type": "flip-flop",
                "state": "off",
                "targets": targets.split(", ")
            }
        elif "&" in id:
            circuit[id[1:]] = {
                "type": "conjunction",
                "targets": targets.split(", "),
                "memory": {

                }
            }
        else:
            circuit[id] = {
                "type": "broadcaster",
                "targets": targets.split(", "),
            }

    # Fill memories for conjunction modules
    for id in circuit:
        for target in circuit[id]["targets"]:
            if target in circuit and circuit[target]["type"] == "conjunction":
                circuit[target]["memory"][id] = "low"

    return circuit


class Circuit:
    def __init__(self, data) -> None:
        self.call_count = 0
        self.high_count = 0
        self.circuit = parse_circuit(data)
        self.queue = []

        self.rx_low_pulse_count = 0
        self.button_press_count = 0

        self.rx_feeder_count = {
            'sj': 0,
            'qq': 0,
            'ls': 0, 
            'bg': 0,
        }

    def send_signal(self, sender_id, signal_type):
        for target_id in self.circuit[sender_id]["targets"]:
            self.queue.append((signal_type, sender_id, target_id))

    def handle_flip_flop(self, handler_id):
        handler = self.circuit[handler_id]
        if handler["state"] == "off":
            self.send_signal(handler_id, "high")
            handler["state"] = "on"
        else:
            self.send_signal(handler_id, "low")
            handler["state"] = "off"
        
    def handle_conjunction(self, handler_id, origin_id, incoming_signal_type):
        handler = self.circuit[handler_id]
        handler["memory"][origin_id] = incoming_signal_type
        outgoing_signal_type = "low" if all(previous_signal == "high" for previous_signal in handler["memory"].values()) else "high"
        self.send_signal(handler_id, outgoing_signal_type)

    def press_button(self):
        self.queue = [("low", "button", "broadcaster")]
        self.rx_low_pulse_count = 0
        self.button_press_count += 1
        while self.queue:
            signal_type, origin_id, handler_id = self.queue.pop(0)
            self.call_count += 1
            self.high_count += signal_type == "high"

            if signal_type == "high" and origin_id in self.rx_feeder_count:
                if self.rx_feeder_count[origin_id] == 0:
                    self.rx_feeder_count[origin_id] = self.button_press_count

            if handler_id in self.circuit:
                handler = self.circuit[handler_id]

                if handler["type"] == "broadcaster":
                    self.send_signal(handler_id, signal_type)

                if handler["type"] == "flip-flop" and signal_type == "low":
                    self.handle_flip_flop(handler_id)

                if handler["type"] == "conjunction":
                    self.handle_conjunction(handler_id, origin_id, signal_type)


def part1():
    c = Circuit(data)
    for _ in range(1000): c.press_button()
    return (c.call_count - c.high_count) * c.high_count


def print_info(c):
    feeds = []

    # From data we observe only one module feeds rx.
    # The module is conjunction and fed by couple of other modules.
    feeds.append(
        {"rx": [k for k in c.circuit if "rx" in c.circuit[k]["targets"]]}
    )
    print("Last layer:", feeds[-1])
    print()

    
    feeds.append({
        t: list(c.circuit[t]["memory"].keys()) for k, v in feeds[-1].items() for t in v
    })
    print("Next layer", feeds[-1])
    print()

    feeds.append({
        t: list(c.circuit[t]["memory"].keys()) for k, v in feeds[-1].items() for t in v
    })
    print("Next layer", feeds[-1])
    print()


from functools import reduce


def part2():
    c = Circuit(data)
    print_info(c)

    # ['sj', 'qq', 'ls', 'bg'] are feeding 'kz' which sends signal to 'rx'
    # We need to find cycles for each of those and take least common divisor
    while not all(n for n in c.rx_feeder_count.values()):
        c.press_button()
    
    return reduce(lambda x, y: x * y, c.rx_feeder_count.values(), 1)


print(part1(), part2())