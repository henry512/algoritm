from typing import List, Optional, Generator, Iterator, Set
import re

import requests as requests


class DNASequenceException(Exception):
    def __init__(self):
        super().__init__(self, "ADN no valido")


class DNASequenceValuesException(Exception):
    def __init__(self):
        super().__init__(self, "Valores de ADN no validos")


class DNA:
    """
    Mutant valida el adn obtenido por medio de una lista List[str], y si esta cumple
    una serie de verificaciones se puede decir que el adn es de un mutante
    Example:
        mutant = Mutant(["ATGCGA", "CAGTGC", "TTATGT", "AGAAGG", "CCCCTA", "TCACTG"])
        mutant.is_mutant()  -> True

    NOTA: Para tener mayor referencia de esta clase leer la consigna.
    """
    def __init__(self, dna: List[str], characters: str = "ACGT"):
        self._matrix = dna
        self._characters = characters
        self._min_length_dna = 4
        self._min_length_character = 4
        self._min_coincidence_mutant = 2
        self._regex_dna_word = re.compile(r'^([%s]*)$' % re.escape(self._characters))
        self._regex_mutant_sequence = re.compile(
            r'([%s])' % re.escape(self._characters) + r'\1{%i}' % (self._min_length_character-1)
        )

    def is_mutant(self) -> bool:
        """
        Ejecuta las validaciones del dna y los caracteres, obtiene de la matriz original
        las N° combinaciones horizonal, vertical y oblicua y los combina para su posterior
        validación, donde ejecutara una expressión regular cuya función es obtener del
        adn los valores que tengan una secuencia >= self._min_coincidence_mutant (2)
        :return:
            [True] si tiene dos(2) o mas secuencias de adn >= self._min_coincidence_mutant (2)
            [False] Si tiene uno(1) o ninguna secuencia de adn >= self._min_coincidence_mutant (2)
        :exception:
            DNASequenceException
            DNASequenceValuesException
        """
        self.validate_dna()

        matriz_unified: Set[str] = set(
            self._matrix + self.get_elements_vertical() + self.get_elements_oblique()
        )

        return len(
            [
                True
                for mutant in matriz_unified
                if len(self._regex_mutant_sequence.findall(mutant)) > 0
            ]
        ) >= self._min_coincidence_mutant

    def validate_dna(self) -> None:
        """
        Verifica que la matriz tenga una longitud >= a self._min_length_dna (4), que la
        longitud de self._characters sea >= a self._min_length_character (4),
        que la longitud de la matriz tenga su equivalente N*N en la longitud de cada
        elemento almacenado en la matriz y que cada elemento de la matriz cumpla con
        la expresión regular, cuya función es validar que existan solo los caracteres
        de self._characters

        :exception:
            DNASequenceException
            DNASequenceValuesException
        """
        if not (len(self._matrix) >= self._min_length_dna):
            raise DNASequenceException
        if not self._min_length_character >= len(self._characters):
            raise DNASequenceException
        if not all([len(self._matrix) == len(value) for value in self._matrix]):
            raise DNASequenceException
        if not all([len(self._regex_dna_word.findall(value)) > 0 for value in self._matrix]):
            raise DNASequenceValuesException

    def get_elements_oblique(self) -> List[str]:
        """
        Construye una lista con todas las posibles combinaciones oblicuas
        (diagonal/contradiagonal) de la matriz de adn, cuyo elementos deban ser
        >= self._min_length_character (4)

        :return:
            List[str] Nueva lista de elementos oblicuos
        """
        def __get_diagonals(dna: List[str]) -> Generator:
            dna_length = len(dna)
            for p in range(2 * dna_length - 1):
                yield [
                    dna[p - q][q]
                    for q in range(max(0, p - dna_length + 1), min(p, dna_length - 1) + 1)
                ]
                yield [
                    dna[dna_length - p + q - 1][q]
                    for q in range(max(0, p - dna_length + 1), min(p, dna_length - 1) + 1)
                ]

        return [
            "".join(value)
            for value in __get_diagonals(self._matrix)
            if len(value) >= self._min_length_character
        ]

    def get_elements_vertical(self) -> List[str]:
        """
        Construye una lista con los elementos de la matriz, desde una pespertiva vertical

        :return:
            List[str] Nueva lista de elementos verticales
        """
        return [
            "".join([value[index] for _, value in enumerate(self._matrix)])
            for index in range(len(self._matrix))
        ]


def prueba(dna: List[str]) -> Generator:
    dna_length: int = len(dna)
    for p in range(2 * dna_length - 1):
        yield [
            dna[p - q][q]
            for q in range(max(0, p - dna_length + 1), min(p, dna_length - 1) + 1)
        ]
        yield [
            dna[dna_length - p + q - 1][q]
            for q in range(max(0, p - dna_length + 1), min(p, dna_length - 1) + 1)
        ]


if __name__ == "__main__":
    other = [
          "CCAGTG",
          "CCAGGC",
          "TAAGCA",
          "CACTGC",
          "CCTCTT",
          "TACTGC"
        ]
    #print(DNA(other).is_mutant())

    other = ["ACGT", "ACGT", "ACGT", "ACGT"]
    #print(DNA(other).is_mutant())  # True

    other = ["ATGCGA", "CAGTGC", "TTATGT", "AGAAGG", "CCCCTA", "TCACTG"]
    #print(DNA(other).is_mutant())  # True

    other = ["ZX", "ZZ"]
    #print(DNA(other, "ZX").is_mutant()) # Exception DNASequenceException

    other = ["QWER", "QWER", "QWER", "QQQA"]
    #print(DNA(other, "QWER").is_mutant())  # Exception DNASequenceValuesException

    other = ["ACGX", "ACGT", "ACGT", "ACGT"]
    #print(DNA(other).is_mutant())  # Exception DNASequenceValuesException

    other = [
        "CCAGTG",
        "CCAGGC",
        "CAAGCA",
        "CACTGC",
        "CCTCTT",
        "CACTGC"
    ]
    #print(DNA(other).is_mutant())
    fail = 0
    success = 0
    while True:
        requests.post("http://localhost:5000/mutant", json={
            "dna": [
                "CCAGTG",
                "CCAGGC",
                "CCAGCA",
                "CACTGC",
                "CCTCTT",
                "CACTGC"
            ]
        })
        requests.post("http://localhost:5000/mutant", json={
            "dna": [
                "CCAGTG",
                "CCAGGC",
                "CCAGCA",
                "CACTGC",
                "CCTCTT",
                "CACTGC"
            ]
        })
        requests.post("http://localhost:5000/mutant", json={
            "dna": [
                "CCAGTG",
                "CCAGGC",
                "CCAGCA",
                "CACTGC",
                "CCTCTT",
                "CACTGC"
            ]
        })
        requests.post("http://localhost:5000/mutant", json={
            "dna": [
                "CCAGTG",
                "CCAGGC",
                "CCAGCA",
                "CACTGC",
                "CCTCTT",
                "CACTGC"
            ]
        })
        requests.post("http://localhost:5000/mutant", json={
            "dna": [
                "CCAGTG",
                "CCAGGC",
                "CCAGCA",
                "CACTGC",
                "CCTCTT",
                "CACTGC"
            ]
        })
        requests.post("http://localhost:5000/mutant", json={
            "dna": [
                "CCAGTG",
                "CCAGGC",
                "CCAGCA",
                "CACTGC",
                "CCTCTT",
                "CACTGC"
            ]
        })
        requests.post("http://localhost:5000/mutant", json={
            "dna": [
                "CCAGTG",
                "CCAGGC",
                "CCAGCA",
                "CACTGC",
                "CCTCTT",
                "CACTGC"
            ]
        })
        requests.post("http://localhost:5000/mutant", json={
            "dna": [
                "CCAGTG",
                "CCAGGC",
                "CCAGCA",
                "CACTGC",
                "CCTCTT",
                "CACTGC"
            ]
        })




