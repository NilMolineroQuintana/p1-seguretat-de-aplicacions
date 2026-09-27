import csv
import os
import sys
from collections import Counter

ALFABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def carrega_freq_catala(ruta_csv=None):
    if ruta_csv is None:
        ruta_csv = os.path.join(os.path.dirname(__file__), "frequencies", "catala.csv")
    freq = {}
    with open(ruta_csv, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            freq[row["lletra"].strip().upper()] = float(row["frequencia"])
    total = sum(freq.values())
    return {k: v / total for k, v in freq.items()}


FREQ_CATALA = carrega_freq_catala()


def neteja(text):
    return "".join(c for c in text.upper() if c in ALFABET)


def index_coincidencia(text):
    n = len(text)
    if n < 2:
        return 0.0
    freq = Counter(text)
    return sum(v * (v - 1) for v in freq.values()) / (n * (n - 1))


def longitud_clau(text, maxim=20, llindar_ic=0.055):
    n = len(text)
    maxim = min(maxim, max(1, n // 2))
    if maxim < 1:
        return 1

    ics = {}
    for k in range(1, maxim + 1):
        columnes = [text[i::k] for i in range(k)]
        valides = [col for col in columnes if len(col) >= 2]
        ics[k] = (
            sum(index_coincidencia(col) for col in valides) / len(valides)
            if valides
            else 0.0
        )

    millor_ic = max(ics.values())
    if millor_ic < llindar_ic:
        return max(ics, key=ics.get)

    # Període fonamental: triem el k més petit amb IC >= 85% del màxim
    candidats = [
        k for k, val in ics.items() if val >= 0.85 * millor_ic and val >= llindar_ic
    ]
    return candidats[0] if candidats else max(ics, key=ics.get)


def desplacament_columna(col, freq_ref=FREQ_CATALA):
    n = len(col)
    if n == 0:
        return 0
    recompte = Counter(col)
    m = len(ALFABET)
    millor_diff = float("inf")
    millor_shift = 0

    for shift in range(m):
        diff = 0.0
        for lletra in ALFABET:
            xifrada = ALFABET[(ALFABET.index(lletra) + shift) % m]
            observada = recompte.get(xifrada, 0) / n
            diff += abs(observada - freq_ref[lletra])
        if diff < millor_diff:
            millor_diff = diff
            millor_shift = shift
    return millor_shift


def troba_clau(text, k, freq_ref=FREQ_CATALA):
    clau = []
    for i in range(k):
        columna = text[i::k]
        clau.append(desplacament_columna(columna, freq_ref))
    return clau


def desxifra(text, clau):
    resultat = []
    m = len(ALFABET)
    for i, c in enumerate(text):
        x = ALFABET.index(c)
        k = clau[i % len(clau)]
        resultat.append(ALFABET[(x - k) % m])
    return "".join(resultat)


def ataca(text, maxim=20, freq_ref=FREQ_CATALA):
    text = neteja(text)
    if not text:
        return 0, [], ""
    k = longitud_clau(text, maxim=maxim)
    clau = troba_clau(text, k, freq_ref)
    missatge = desxifra(text, clau)
    return k, clau, missatge


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Us: python corregit_ia.py criptograma.txt")
        sys.exit(1)

    contingut = open(sys.argv[1], encoding="utf-8").read()
    k, clau, missatge = ataca(contingut)
    clau_text = "".join(ALFABET[c] for c in clau)

    print(f"Longitud: {k}")
    print(f"Clau: {clau_text}")
    print(f"Text desxifrat:\n{missatge}")
