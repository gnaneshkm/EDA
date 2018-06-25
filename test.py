from pyeda.inter import *

f = expr("a & b | a & c | b & c")

f = expr2bdd(f)