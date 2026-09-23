import re
import sys

# Mida màxima dels grams a cercar; l'opció --max N la canvia (per defecte 5)
MAX_GRAMA = 5

nom_arxiu = None
mida_maxima = MAX_GRAMA
i = 1
while i < len(sys.argv):
    if sys.argv[i] == "--max":
        mida_maxima = int(sys.argv[i + 1])
        i += 2
    else:
        nom_arxiu = sys.argv[i]
        i += 1

if nom_arxiu is None:
    print("Us: python analitza.py [--max N] criptograma.txt")
    sys.exit(1)

criptograma = open(nom_arxiu, "r").read()

# Si el criptograma conté nombres (criptograma B), cada nombre és un símbol;
# altrament cada lletra és un símbol (criptogrames A i C)
if re.search(r"\d", criptograma):
    simbols = re.findall(r"\d+", criptograma)
else:
    simbols = [c.upper() for c in criptograma if c.isalpha()]

# Comptar la freqüència de cada símbol del criptograma
frequencies = {}
for simbol in simbols:
    if simbol in frequencies:
        frequencies[simbol] += 1
    else:
        frequencies[simbol] = 1

# Calcular la longitud total del criptograma
longitud = len(simbols)

# Ordenar les freqüències en ordre descendent
frequencies_ordenades = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)

# Símbols més freqüents
mes_frequents = [simbol for simbol, _ in frequencies_ordenades[:10]]

# Índex de coincidència
ic = sum(vegades * (vegades - 1) for vegades in frequencies.values()) / (
    longitud * (longitud - 1)
)

# Bigrames, trigrames i grams més llargs repetits, amb les seves posicions i les
# distàncies entre ocurrències consecutives
repeticions = {}
for mida in range(2, mida_maxima + 1):
    posicions = {}
    for i in range(longitud - mida + 1):
        grama = tuple(simbols[i : i + mida])
        posicions.setdefault(grama, []).append(i)

    repeticions[mida] = [
        (grama, trobades)
        for grama, trobades in posicions.items()
        if len(trobades) >= 2
    ]
    repeticions[mida].sort(key=lambda x: (-len(x[1]), x[0]))

# Resum estadístic
print(f"Longitud total del criptograma: {longitud}")
print(f"Nombre de simbols diferents: {len(frequencies)}")
print(f"Index de coincidencia: {ic:.4f}")
print(f"Simbols mes frequents: {' '.join(mes_frequents)}")

# Taula de freqüències
print("\nTaula de frequencies (simbol | vegades | frequencia relativa):")
for simbol, vegades in frequencies_ordenades:
    print(f"{simbol} | {vegades} | {vegades / longitud:.2%}")

# Grams repetits
print("\nGrames repetits (grama | ocurrencies | posicions | distancies):")
for mida in range(2, mida_maxima + 1):
    for grama, trobades in repeticions[mida]:
        distancies = [
            trobades[j + 1] - trobades[j] for j in range(len(trobades) - 1)
        ]
        if all(len(simbol) == 1 for simbol in grama):
            grama_text = "".join(grama)
        else:
            grama_text = " ".join(grama)
        print(
            f"[{mida}-gram] {grama_text!r} | {len(trobades)} | {trobades} | {distancies}"
        )