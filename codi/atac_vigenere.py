import csv
import math
import os
import sys
from collections import Counter


def carrega_alfabet_i_freq(csv_path):
    alfabet = []
    freq = {}
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        noms = reader.fieldnames
        for row in reader:
            lletra = row[noms[0]].strip().upper()
            alfabet.append(lletra)
            freq[lletra] = float(row[noms[1]])
    total = sum(freq.values())
    return alfabet, {lletra: freq[lletra] / total for lletra in alfabet}


def neteja(text, alfabet):
    conjunt_alfabet = set(alfabet)
    return "".join(c for c in text.upper() if c in conjunt_alfabet)


def index_coincidencia(text):
    n = len(text)
    if n < 2:
        return 0.0
    freq = Counter(text)
    return sum(v * (v - 1) for v in freq.values()) / (n * (n - 1))


def ic_per_periode(text, k):
    total = 0.0
    n = 0
    for i in range(k):
        col = text[i::k]
        if len(col) >= 2:
            total += index_coincidencia(col)
            n += 1
    return total / n if n else 0.0


def grams_repetits(text, mida):
    posicions = {}
    for i in range(len(text) - mida + 1):
        grama = text[i : i + mida]
        posicions.setdefault(grama, []).append(i)
    return {g: p for g, p in posicions.items() if len(p) >= 2}


def kasiski(text, mida, maxim):
    distancies = []
    for grama, pos in grams_repetits(text, mida).items():
        for a, b in zip(pos, pos[1:]):
            distancies.append(b - a)
    if not distancies:
        return [], {}
    mcd = distancies[0]
    for d in distancies[1:]:
        mcd = math.gcd(mcd, d)
    divisors = {
        k: sum(1 for d in distancies if d % k == 0) for k in range(2, maxim + 1)
    }
    return distancies, divisors


def desplacaments_columna(col, freq_catala, alfabet, quants=3):
    m = len(alfabet)
    n = len(col)
    if n == 0:
        return []
    recompte = Counter(col)
    resultats = []
    for desplacament in range(m):
        diferencia = 0.0
        for lletra in alfabet:
            xifrada = alfabet[(alfabet.index(lletra) + desplacament) % m]
            observada = recompte.get(xifrada, 0) / n
            diferencia += abs(observada - freq_catala[lletra])
        resultats.append((diferencia, desplacament))
    resultats.sort()
    return resultats[:quants]


def desxifra(text, clau, alfabet):
    m = len(alfabet)
    return "".join(
        alfabet[(alfabet.index(text[i]) - clau[i % len(clau)]) % m]
        for i in range(len(text))
    )


def embolica(text, ample):
    return "\n".join(text[i : i + ample] for i in range(0, len(text), ample))


def tria_periode_fonamental(candidats, ics):
    if not candidats:
        return None
    candidats = sorted(candidats)
    base = candidats[0]
    if all(c % base == 0 for c in candidats):
        return base
    return max(candidats, key=lambda k: ics[k])


def main():
    if len(sys.argv) < 2:
        print("Us: python atac_vigenere.py criptograma.txt")
        return

    contingut = open(sys.argv[1], encoding="utf-8").read()
    if any(c.isdigit() for c in contingut) and not any(c.isalpha() for c in contingut):
        print("Es tracta d'un criptograma de simbols no alfabetics.")
        print("Aquest atac esta pensat per a xifratges de Vigenere.")
        return

    csv_path = os.path.join(os.path.dirname(__file__), "frequencies", "catala.csv")
    if len(sys.argv) >= 3:
        csv_path = sys.argv[2]
    alfabet, freq_catala = carrega_alfabet_i_freq(csv_path)

    text = neteja(contingut, alfabet)
    if not text:
        print("Criptograma buit.")
        return

    maxim_k = min(20, max(1, len(text) // 2))
    ics = {k: ic_per_periode(text, k) for k in range(1, maxim_k + 1)}

    print(f"Longitud: {len(text)}")
    print(f"IC global: {index_coincidencia(text):.4f}")

    distancies, divisors = kasiski(text, mida=3, maxim=maxim_k)
    if distancies:
        mcd = distancies[0]
        for d in distancies[1:]:
            mcd = math.gcd(mcd, d)
        compat = [k for k in range(2, maxim_k + 1) if divisors[k] >= 2]
        print(f"Kasiski: {len(distancies)} distancies; mcd = {mcd}")
        print("Divisors compatibles amb mes d'una distancia: "
              + ", ".join(str(k) for k in compat))

    llindar = 0.055
    candidats = [k for k in range(1, maxim_k + 1) if ics[k] >= llindar]

    print("\nPossibles longituds de clau (IC mitjana per columna):")
    for k in range(1, maxim_k + 1):
        marca = "   <- candidata" if k in candidats else ""
        print(f"  k={k:>2}: {ics[k]:.4f}{marca}")

    k = tria_periode_fonamental(candidats, ics)
    if k is None:
        k = max(ics, key=ics.get)
    if len(candidats) > 1 and all(c % k == 0 for c in candidats if c != k):
        multiples = ", ".join(str(c) for c in candidats if c != k)
        print(f"\nLongitud escollida: {k} (les candidates {multiples} son multiples: "
              "periode fonamental)")
    else:
        print(f"\nLongitud escollida: {k}")

    candidats_per_columna = [
        desplacaments_columna(text[i::k], freq_catala, alfabet, quants=3)
        for i in range(k)
    ]

    print("\nPossibles desplacaments de cada posicio "
          "(millor coincidencia de frequencies):")
    for i, candidats_col in enumerate(candidats_per_columna):
        parts = " ".join(f"{d:>2}->{alfabet[d]}" for _, d in candidats_col)
        print(f"  posicio {i}: {parts}")

    clau = [candidats_col[0][1] for candidats_col in candidats_per_columna]
    paraules = "".join(alfabet[d] for d in clau)
    print(f"\nClau candidata: {paraules}")

    missatge = desxifra(text, clau, alfabet)
    print("\nText desxifrat:\n")
    print(embolica(missatge, 80))


if __name__ == "__main__":
    main()