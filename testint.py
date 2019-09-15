from math import *

def max_number(n):
    digit_count = int(log(abs(n+1),10)) + 1 
    digits = sorted([(n / 10 ** (x - 1) % 10)  for x in range(digit_count,0,-1) ], reverse=True)
    return reduce(lambda x, y:10*x + y, digits)



