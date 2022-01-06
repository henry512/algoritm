from typing import List, Optional


def execute(base: int, caracter: str) -> str:
    result: Optional[List[str]] = []
    for i in range(1, base+1):
        result.append(caracter * i + "\n")
    return "".join(result)


if __name__ == "__main__":
    print(execute(5, "X"))
