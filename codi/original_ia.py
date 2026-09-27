import sys
from collections import Counter

ALFABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def neteja(text):
    return "".join(c for c in text.upper() if c.isalpha())


def index_coincidencia(text):
    n = len(text)
    freq = Counter(text)
    return sum(v * (v - 1) for v in freq.values()) / (n * (n - 1))


def longitud_clau(text, maxim=20):
    millor_k = 1
    millor_ic = 0
    for k in range(1, maxim + 1):
        columnes = [text[i::k] for i in range(k)]
        ic_mitja = sum(
            index_coincidencia(col) for col in columnes
        ) / k
        if ic_mitja > millor_ic:
            millor_ic = ic_mitja
            millor_k = k
    return millor_k


def desplacament_columna(col):
    mes_frequent = Counter(col).most_common(1)[0][0]
    return (
        ALFABET.index(mes_frequent)
        - ALFABET.index("E")
    ) % 26


def troba_clau(text, k):
    clau = []
    for i in range(k):
        columna = text[i::k]
        clau.append(desplacament_columna(columna))
    return clau


def desxifra(text, clau):
    resultat = []
    for i, c in enumerate(text):
        x = ALFABET.index(c)
        k = clau[i % len(clau)]
        resultat.append(ALFABET[(x - k) % 26])
    return "".join(resultat)


def ataca(text):
    text = neteja(text)
    k = longitud_clau(text)
    clau = troba_clau(text, k)
    missatge = desxifra(text, clau)
    return k, clau, missatge


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Us: python original_ia.py criptograma.txt")
        sys.exit(1)

    contingut = open(sys.argv[1], encoding="utf-8").read()
    k, clau, missatge = ataca(contingut)
    clau_text = "".join(ALFABET[c] for c in clau)

    print(f"Longitud: {k}")
    print(f"Clau: {clau_text}")
    print(f"Text desxifrat:\n{missatge}")
