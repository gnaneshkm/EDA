import sys
from pyeda.inter import *

def readNetlist(file):
    nets = int(file.readline().strip('\n'))
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
        mapping[name] = chr(int(net) + 64)

    # read gates
    gates = []
    for line in file.readlines():
        bits = line.split()
        gate = bits.pop(0)
        bits = [int(x) + 64 for x in bits]
        ports = list(map(chr, bits))
        gates.append((gate, ports))

    return inputs, outputs, mapping, gates


# read netlists
inputs1, outputs1, mapping1, gates1 = readNetlist(open("xor2_nand.net", "r"))
inputs2, outputs2, mapping2, gates2 = readNetlist(open("xor2_nand_wrong.net", "r"))


def trivial_bdd(inputs):
    trivial_bdd_inputs = []
    for input in inputs:
        trivial_bdd_inputs.append({input: (1, 0)})
    return trivial_bdd_inputs

def ITE_logic(logic, a, b):
    if logic == "inv":
        return (a, False, True)
    elif logic == "and":
        return (a, b, False)
    elif logic == "or":
        return (a, True, b)
    elif logic == "xor":
        return (a, not b, b)

a = True
b = False
logic = "and"
ITE = ITE_logic(logic, a, b)


trivial_bdd_1 = trivial_bdd(inputs1)
trivial_bdd_2 = trivial_bdd(inputs2)

gates1_ite = []
for gate in gates1:
    logic = gate[0]
    a, b, c = gate[1]
    gates1_ite.append(ITE_logic(logic, a, b))


print(trivial_bdd_1)
































