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


def press_button(circuit):
    queue = [("low", "button", "broadcaster")]
    call_count = 0
    high_count = 0

    def send_signal(sender, sender_id, signal_type):
        for target_id in sender["targets"]:
            queue.append((signal_type, sender_id, target_id))

    def handle_flip_flop(handler, handler_id):
        if handler["state"] == "off":
            handler["state"] = "on"
            send_signal(handler, handler_id, "high")
        else:
            handler["state"] = "off"
            send_signal(handler, handler_id, "low")

    def handle_conjunction(handler, handler_id, origin_id, incoming_signal_type):
        handler["memory"][origin_id] = incoming_signal_type
        outgoing_signal_type = "low" if all(previous_signal == "high" for previous_signal in handler["memory"].values()) else "high"
        send_signal(handler, handler_id, outgoing_signal_type)

    while queue:
        signal_type, origin_id, handler_id = queue.pop(0)
        call_count += 1
        high_count += signal_type == "high"

        if handler_id in circuit:
            handler = circuit[handler_id]

            if handler["type"] == "broadcaster":
                send_signal(handler, handler_id, signal_type)

            if handler["type"] == "flip-flop" and signal_type == "low":
                handle_flip_flop(handler, handler_id)

            if handler["type"] == "conjunction":
                handle_conjunction(handler, handler_id, origin_id, signal_type)

    return call_count, high_count


def part1():            
    t = 0
    h = 0
    circuit = parse_circuit(data)
    
    for _ in range(1000):
        x, y = press_button(circuit)
        t += x
        h += y
    
    return (t -h) * h


print(part1())
