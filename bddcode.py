import sys


def readNetlist(file):
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

        net, name = line.split()
        mapping[name] = int(net)

    # read gates
    gates = []
    for line in file.readlines():
        bits = line.split()
        gate = bits.pop(0)
        ports = map(int, bits)
        gates.append((gate, ports))




    return inputs, outputs, mapping, gates


# read netlists
inputs1, outputs1, mapping1, gates1 = readNetlist(open("xor2.net", "r"))
inputs2, outputs2, mapping2, gates2 = readNetlist(open("xor2_nand.net", "r"))

def ITE_trivial(f, g, h):
    if (g == h):
        return g
    elif (g == True && h == False):
        return  f
    elif (f == True):
        return g
    else
        return h

def cofactor(f, x):
    return ITE()



























