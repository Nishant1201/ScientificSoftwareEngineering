import sys

p = float(sys.argv[1])
delta = float(sys.argv[2])

from math import exp
result = delta*exp(-p)

print(result)