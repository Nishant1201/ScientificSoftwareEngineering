import argparse
from math import exp

parser = argparse.ArgumentParser()
parser.add_argument('--p', default=1.0, type=float)
parser.add_argument('--delta', default=0.1, type=float)

args = parser.parse_args()
p = args.p
delta = args.delta

result = delta*exp(-p)

print(result)