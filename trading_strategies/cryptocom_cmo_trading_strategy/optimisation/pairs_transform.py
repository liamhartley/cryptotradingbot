with open('/Users/liamhartley/PycharmProjects/cryptotradingbot/pairs_raw.txt') as f:
    pairs = []
    lines = f.readlines()
    for line in lines:
        print(line)
        if '/' in line:
            pairs.append(line.replace('/','_'))

print(pairs)