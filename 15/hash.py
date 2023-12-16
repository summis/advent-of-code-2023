with open("input") as f:
    data = f.read().split(",")


def hash(s):
    tot = 0
    for c in s:
        tot = (tot + ord(c)) * 17 % 256
    return tot


def part1(instructions):
    print(sum(hash(x) for x in  instructions))


def part2(instructions):
    boxes = {
        i : [] for i in range(256)
    }
    lenses = {}


    for instruction in instructions:

        # Removing lense
        if "-" in instruction:
            label = instruction[:-1]
            box = hash(label)
            
            if label in boxes[box]:
                boxes[box].remove(label)
                del lenses[label]

        # Adding lense
        if "=" in instruction:
            label = instruction[:-2]
            box = hash(label)
            focal = int(instruction[-1])

            lenses[label] = focal
        
            if label not in boxes[box]:
                boxes[box].append(label)

    total = 0
    for box, lenses_in_box in boxes.items():
        for i, lense in enumerate(lenses_in_box): 
            total += (box + 1) *  (i + 1) * lenses[lense]

    print(total)


part1(data)
part2(data)