def is_valid(update, rules):
    updated = {update[0]}
    for n in update[1:]:
        rule = rules[n]
        if updated & rule:
            return False
        updated.add(n)
    return True


def fix_update(update, rules):
    start = 0
    while start < len(update):
        i = start + 1
        while i < len(update):
            rule = rules[update[i]]
            if update[start] in rule:
                update[start], update[i] = update[i], update[start]
            i += 1
        start += 1
    return update


def solve(data):
    rules, updates = parse(data)

    sum = 0
    sum2 = 0
    for update in updates:
        if is_valid(update, rules):
            sum += update[len(update) // 2]
        else:
            update = fix_update(update, rules)
            sum2 += update[len(update) // 2]
    return sum, sum2
