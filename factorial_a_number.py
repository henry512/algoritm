import functools
import math
import operator
from typing import List


def execute(number: int) -> List[int]:
    factorials: List[int] = []
    divisor: int = 2
    dividendo: int = number

    while True:
        temp: float = dividendo / divisor

        if math.modf(temp)[0] > .1:
            factorials.append(int(dividendo))
            break

        factorials.append(int(divisor))
        dividendo = int(temp)

    return factorials


if __name__ == "__main__":
    result: List[int] = execute(24)
    print(result)
    print(functools.reduce(operator.mul, result))  # equivalent functools.reduce(lambda a,b: a*b, result)


# 24=  24/2=12 [2],   12/2=6 [2],   6/2=3 [2],  3/2=1.5   [3]
# el divisor se toma en cuenta [2], si el resultado no es un entero, se toma como ultimo valor
# el dividendo [3]
