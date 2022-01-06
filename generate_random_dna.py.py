import random

def generador_de_dna():
    dnas = []
    for w in range(1000):
        dna = []
        for i in range(6):
            fila = ''
            for j in range(6):
                letra = random.choice(['A','T', 'C', 'G', "X"])
                fila += letra
            dna.append(fila)
        dnas.append(dna)
    return random.choice(dnas)

print(generador_de_dna())