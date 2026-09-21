import argparse
import csv
import os
from collections import Counter

# --- Llegir arguments ---
parser = argparse.ArgumentParser(description="Atac assistit a substitució")
parser.add_argument('filename')
args = parser.parse_args()

# --- Llegir criptograma ---
text: str = open(args.filename, "r").read().upper().strip()
solo_letras = [c for c in text if c.isalpha()]

# --- Llegir freqüències del català ---
freq_catala = {}
csv_path = os.path.join(os.path.dirname(__file__), "freqüencies", "catala.csv")
with open(csv_path, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        freq_catala[row["lletra"]] = float(row["frequencia"])

# --- Calcular freqüències del criptograma ---
def calcular_freq(letras):
    total = len(letras)
    comptador = Counter(letras)
    freq = {}
    for lletra, count in comptador.most_common():
        freq[lletra] = (count, count / total * 100)
    return freq

# --- Mostrar freqüències comparades ---
def mostrar_freq(freq_cripto):
    catala_ordenat = sorted(freq_catala.items(), key=lambda x: -x[1])
    cripto_ordenat = sorted(freq_cripto.items(), key=lambda x: -x[1][1])

    print("\n  CRIPTOGRAMA              CATALÀ")
    print("  Lletra  Abs   Rel%       Lletra  Rel%")
    print("  " + "-" * 40)
    for i in range(max(len(cripto_ordenat), len(catala_ordenat))):
        part_c = ""
        part_k = ""
        if i < len(cripto_ordenat):
            ll, (ab, rel) = cripto_ordenat[i]
            part_c = f"  {ll:>4}   {ab:>4}  {rel:>5.1f}%"
        else:
            part_c = " " * 22
        if i < len(catala_ordenat):
            ll_k, rel_k = catala_ordenat[i]
            part_k = f"      {ll_k:>4}  {rel_k:>5.2f}%"
        print(part_c + part_k)

# --- Mostrar text parcial ---
def mostrar_text(text, subs):
    resultat = []
    for c in text:
        if c.isalpha():
            if c in subs:
                resultat.append(subs[c].lower())
            else:
                resultat.append("_")
        else:
            resultat.append(c)
    print("\nText parcial:\n")
    print("".join(resultat))

# --- Mostrar substitucions actuals ---
def mostrar_subs(subs):
    if not subs:
        print("\n  (cap substitució definida)")
        return
    print("\n  Substitucions actuals:")
    for orig, dest in sorted(subs.items()):
        print(f"    {orig} -> {dest}")

# --- Bucle principal ---
freq_cripto = calcular_freq(solo_letras)
subs = {}  # clau original -> lletra desxifrada

print("=" * 50)
print("  ASSISTENT DE CRIPTOANÀLISI")
print("  Substitució monoalfabètica")
print("=" * 50)

mostrar_freq(freq_cripto)

while True:
    mostrar_subs(subs)
    mostrar_text(text, subs)

    print("\nComandes:")
    print("  X Y   -> substituir X per Y")
    print("  -X    -> eliminar substitució de X")
    print("  freq  -> mostrar freqüències")
    print("  q     -> sortir")

    entrada = input("\n> ").strip().upper()

    if entrada == "Q":
        break
    elif entrada == "FREQ":
        mostrar_freq(freq_cripto)
    elif entrada.startswith("-") and len(entrada) == 2:
        lletra = entrada[1]
        if lletra in subs:
            del subs[lletra]
            print(f"  Eliminada substitució de {lletra}")
        else:
            print(f"  {lletra} no té substitució")
    elif len(entrada.split()) == 2:
        parts = entrada.split()
        orig, dest = parts[0], parts[1]
        if len(orig) == 1 and len(dest) == 1 and orig.isalpha() and dest.isalpha():
            subs[orig] = dest
            print(f"  {orig} -> {dest}")
        else:
            print("  Format incorrecte. Usa: X Y")
    else:
        print("  Comanda no reconeguda")