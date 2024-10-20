# Create a hasse diagram for divisibilty of a number
NUMBER = 60

print("Hasse Diagramm for Divisibility of", NUMBER)

divs = { i: [] for i in range(1, NUMBER + 1) if NUMBER % i == 0 }
dis = sorted(divs.keys())

for i in divs:
    for j in divs:
        if i % j == 0: divs[i].append(j)

hasse = { }

for i in dis:
    there = { *divs[i] } - { i }
    have = set()
    con = []

    for j in sorted(there, reverse = True):
        have.update(divs[j])
        con.append(j)
        if not there - have: break

    hasse[i] = con

rev = { i: [] for i in hasse }
for i in hasse:
    for j in hasse[i]:
        rev[j].append(i)

levels = [[dis[0]]]
diz = rev[dis[0]]
while diz:
    nex = set()
    for i in diz:
        nex.update(rev[i])
    levels.append(sorted(diz))
    diz = nex

for i in levels[::-1]:
    l = []
    for j in i:
        l.append(f"{j} -> {rev[j]}")
    print(" | ".join(l))
