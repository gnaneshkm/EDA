from pyeda.inter import *
from dd.autoref import BDD

bdd = BDD()
bdd.declare('x', 'y', 'z', 'w')


f = expr("a & b | a & c | b & c")
f = expr2bdd(f)

print(f)
