channels = list()
with open('channels.txt') as f:
    for line in f.readlines():
        channels.append(line)

tokens = list()
with open('tokens.txt') as f:
    for line in f.readlines():
        tokens.append(line)

print(type(tokens[0]))
