deck = list(range(10007))
lines = open("input.txt").read().splitlines()
for line in lines:
    if line.startswith("deal with increment"):
        increment = int(line.split(" ")[-1])
        new = [0] * len(deck)
        for i, n in enumerate(deck):
            new[(i * increment) % len(deck)] = n
        deck = new
    elif line.startswith("cut"):
        n = int(line.split(" ")[-1])
        if n < 0:
            n = len(deck) + n
        deck = deck[n:] + deck[:n]
    elif line.startswith("deal into new stack"):
        deck = deck[::-1]
    else:
        raise Exception("bad instruction")

print(deck.index(2019))
