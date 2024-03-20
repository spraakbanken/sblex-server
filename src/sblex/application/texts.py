def inits(s):
    xs = []
    for i in range(1, len(s) + 1):
        xs.append((s[:i], s[i:]))
    return xs
