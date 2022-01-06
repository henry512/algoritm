from typing import List


# def execute(max_terminal_number: int):
#     if max_terminal_number == 0:
#         return 0
#     if max_terminal_number == 1:
#         return 1
#     return execute(max_terminal_number-1) + execute(max_terminal_number-2)

def execute(max_terminal_number: int) -> List[int]:
    if max_terminal_number in (0, 1):
        return [max_terminal_number]

    result: List[int] = [0 for _ in range(max_terminal_number)]
    result[0] = 1
    result[1] = 2
    first_number: int = result[0]
    second_number: int = result[1]

    for index in range(2, max_terminal_number):
        result[index] = first_number + second_number
        first_number = result[index-1]
        second_number = result[index]

    return result


if __name__ == "__main__":
    print(execute(10))

# even fibonacci of number 10
# return [1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
# 1+2=3,   2+3=5,    3+5=8,    5+8=13,    8+13=21,     13+21=34    ......

