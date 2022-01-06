from typing import List


def execute(range_number_multiplies: List[int], max_number_of_multiplies_result: int) -> int:
    result: int = 0
    num_multiplies: int = 1
    continuar: bool = True
    success_max_multiplies: List[bool] = [False for _ in range_number_multiplies]

    while continuar:
        temporal_result: int = 0
        for num in range(0, len(range_number_multiplies)):
            result_multiplies = range_number_multiplies[num] * num_multiplies
            if result_multiplies < max_number_of_multiplies_result:
                temporal_result += result_multiplies
            else:
                success_max_multiplies[num] = True

        continuar = not all(success_max_multiplies)
        num_multiplies += 1
        result += temporal_result

    return result


if __name__ == "__main__":
    print(execute([3, 5], 10))
