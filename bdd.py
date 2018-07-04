import sys, re

def readNetlist(file, offset):
    nets = int(file.readline())
    inputs = file.readline().split()
    inputs.sort()
    outputs = file.readline().split()
    outputs.sort()

    # read mapping
    mapping = {}
    while True:
        line = file.readline().strip()
        if not line:
            break

        net,name = line.split()
        mapping[name] = int(net) + offset

    # read gates
    gates = []
    for line in file.readlines():
        bits = line.split()
        gate = bits.pop(0)
        ports = list(map(int,bits))
        ports = [p + offset for p in ports]
        gates.append((gate,ports))
        
    return nets,inputs,outputs,mapping,gates

# read netlists
nets1, inputs1,outputs1,mapping1,gates1 = readNetlist(open("adder4.net", "r"), 2)
nets2, inputs2,outputs2,mapping2,gates2 = readNetlist(open("adder4_rc.net", "r"),  2 + nets1)


# add your code here!


def topVariable(f):# to find the top variable for spliting
    try:
        return int(f[0][1:])
    except:
        return f

def BDD(x, A, B):
    if A == B: return A
    return ['x' + str(x), A, B]

def ITE(f, g, h):
    if f == 1: return g
    if f == 0: return h
    if g == h: return g
    if g == 1 and h == 0: return f

    x = max(topVariable(f), topVariable(g), topVariable(h))

    f0, f1 = Cofactors(f, x)
    g0, g1 = Cofactors(g, x)
    h0, h1 = Cofactors(h, x)

    branchX_0 = ITE(f0, g0, h0)
    branchX_1 = ITE(f1, g1, h1)

    return BDD(x, branchX_0, branchX_1)


def Cofactors(f, x):
    if f == 1 or f == 0: return f, f

    if x > topVariable(f): return f, f

    if x == topVariable(f): return f[1], f[2]  # A,B

    if x < topVariable(f):
        A0, A1 = Cofactors(f[1], x)  # A
        B0, B1 = Cofactors(f[2], x)  # B
        BDD0 = BDD(x, A0, B0)
        BDD1 = BDD(x, A1, B1)
        return BDD0, BDD1


def not_o(nets):
    return nets[1], ITE(BDDs[nets[0]], 0, 1)


def or_o(nets):
    return nets[2], ITE(BDDs[nets[0]], 1, BDDs[nets[1]])


def and_o(nets):
    return nets[2], ITE(BDDs[nets[0]], BDDs[nets[1]], 0)


def xor_o(nets):
    return nets[2], ITE(BDDs[nets[0]], ITE(BDDs[nets[1]], 0, 1), BDDs[nets[1]])


GATE = {
    "inv": not_o,
    "or": or_o,
    "and": and_o,
    "xor": xor_o
}

BDDs = {}
def constructBDD(mappingX, inputsX, gatesX):
    inputs = [mappingX[inX] for inX in inputsX]

    for inX in inputs:
        bdd = BDD(inX, 1, 0)
        BDDs[bdd[0]] = bdd

    while len(gatesX) > 0:
        for gate in gatesX:
            if gate[1][0] in inputs and gate[1][len(gate[1]) - 2] in inputs:
                inputs.append(gate[1][len(gate[1]) - 1])

                f, bdd = GATE[gate[0]](['x' + str(g) for g in gate[1]])
                BDDs[f] = bdd
                gatesX.remove(gate)



if len(inputs1) == len(inputs2) and len(outputs1) == len(outputs2):
    constructBDD(mapping1, inputs1, gates1)
    constructBDD(mapping2, inputs2, gates2)

    for out1 in outputs1:
        bdd1 = str(BDDs['x' + str(mapping1[out1])])
        bdd2 = str(BDDs['x' + str(mapping2[out1])])

        for varX, varY in zip(re.findall(r'x\d+', bdd1), re.findall(r'x\d+', bdd2)):
            bdd2 = bdd2.replace(varY, varX)

        if bdd1 == bdd2:
            print(out1, ": OK")
        else:
            print(out1, ": Not OK")