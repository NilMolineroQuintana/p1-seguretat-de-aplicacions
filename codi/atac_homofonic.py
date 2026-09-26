import csv
import os
import re
import sys
from collections import Counter

# --- Llegir arguments ---
if len(sys.argv) < 2:
    print("Us: python atac_homofonic.py criptograma.txt")
    sys.exit(1)

contingut = open(sys.argv[1], encoding="utf-8").read()

# --- Llegir frequencies del catala ---
freq_catala = {}
csv_path = os.path.join(os.path.dirname(__file__), "frequencies", "catala.csv")
with open(csv_path, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        freq_catala[row["lletra"].strip().upper()] = float(row["frequencia"])

# --- Parsejar criptograma ---
# '/' separa paraules, dins de cada paraula els codis son nombres separats per espais
paraules = []
for bloc in contingut.replace("\n", " ").split("/"):
    codis = re.findall(r"\d+", bloc)
    if codis:
        # normalitzar a dos digits
        paraules.append([c.zfill(2) for c in codis])

tots_simbols = [s for p in paraules for s in p]
comptador = Counter(tots_simbols)
total_simbols = len(tots_simbols)

print(f"Longitud: {total_simbols} simbols")
print(f"Codis diferents: {len(comptador)}")
print(f"Paraules: {len(paraules)}")

# --- Estat ---
subs = {}           # codi -> lletra
historial = []      # llista de snapshots anteriors
vista_doble = False


# ============================================================
#  Funcions d'analisi
# ============================================================

def freq_codis():
    """Mostra la frequencia de cada codi i la seva hipotesi actual."""
    print("\n  codi  vegades     %   hipotesi")
    print("  " + "-" * 34)
    for codi, vegades in comptador.most_common():
        hip = subs.get(codi, "-")
        print(f"  {codi}   {vegades:>5}  {vegades / total_simbols * 100:>5.2f}%   {hip}")


def freq_lletres():
    """Frequencia agrupada per lletra (suma dels homofonics) vs catala."""
    # agrupar codis per lletra
    per_lletra = {}
    for codi, lletra in subs.items():
        per_lletra.setdefault(lletra, []).append(codi)

    catala_ordenat = sorted(freq_catala.items(), key=lambda x: -x[1])

    print("\n  lletra   % text   % catala   codis assignats")
    print("  " + "-" * 48)
    for lletra, esperat in catala_ordenat:
        codis = sorted(per_lletra.get(lletra, []))
        pct = sum(comptador[c] for c in codis) / total_simbols * 100
        marca = "  <-- massa?" if pct > 1.6 * esperat + 1 else ""
        codis_txt = " ".join(codis) if codis else "-"
        print(f"  {lletra}      {pct:>5.1f}     {esperat:>5.2f}     {codis_txt}{marca}")

    lliure = sum(v for c, v in comptador.items() if c not in subs)
    print(f"\n  Text sense assignar: {lliure / total_simbols * 100:.1f}%")


def context_codi(codi):
    """Mostra els veins de cada aparicio d'un codi dins les paraules."""
    if codi not in comptador:
        print(f"  El codi {codi} no apareix al criptograma.")
        return
    print(f"\n  Context de {codi} ({comptador[codi]} aparicions):")
    print(f"  {'abans':>5} [{codi}] {'despres':<7}  paraula                  text parcial")
    print("  " + "-" * 64)
    for p in paraules:
        for i, s in enumerate(p):
            if s == codi:
                abans = p[i - 1] if i > 0 else "^"
                despres = p[i + 1] if i < len(p) - 1 else "$"
                codis_txt = " ".join(p)
                parcial = "".join(subs.get(c, "_") for c in p)
                print(f"  {abans:>5} [{codi}] {despres:<7}  {codis_txt:<25}{parcial}")
    print("  (^ = inici, $ = final de paraula)")


def llista_paraules(mida):
    """Llista les paraules de N simbols."""
    trobades = [p for p in paraules if len(p) == mida]
    if not trobades:
        print(f"  No hi ha paraules de {mida} simbols.")
        return
    print(f"\n  Paraules de {mida} simbols ({len(trobades)}):")
    for p in trobades:
        codis_txt = " ".join(p)
        parcial = "".join(subs.get(c, "_") for c in p)
        print(f"    {codis_txt:<{3 * mida}}  {parcial}")


def encaixa(paraula):
    """Cerca paraules xifrades on 'paraula' es compatible amb les hipotesis."""
    paraula = paraula.upper()
    trobades = []
    for p in paraules:
        if len(p) != len(paraula):
            continue
        ok = True
        vist = {}
        for codi, lletra in zip(p, paraula):
            # si el codi ja te hipotesi, ha de coincidir
            if codi in subs and subs[codi] != lletra:
                ok = False
                break
            # si el codi ja l'hem vist en aquesta paraula, ha de ser la mateixa lletra
            if codi in vist and vist[codi] != lletra:
                ok = False
                break
            vist[codi] = lletra
        if ok:
            trobades.append(p)
    if not trobades:
        print(f"  '{paraula}' no encaixa amb cap paraula.")
        return
    print(f"\n  '{paraula}' es compatible amb {len(trobades)} paraula(es):")
    for p in trobades:
        parcial = "".join(subs.get(c, "_") for c in p)
        print(f"    {' '.join(p):<34}  ara: {parcial}")


# ============================================================
#  Sortida de text
# ============================================================

AMPLADA = 78


def mostrar_text_compacte():
    """Mostra el text parcial: majuscula=coneguda, _=pendent."""
    linia = ""
    for p in paraules:
        mot = "".join(subs.get(c, "_") for c in p)
        if len(linia) + len(mot) + 1 > AMPLADA:
            print("  " + linia)
            linia = ""
        linia += mot + " "
    if linia:
        print("  " + linia)


def mostrar_text_doble():
    """Vista doble: codis a dalt, lletres a sota."""
    dalt, baix = "", ""
    for p in paraules:
        codis = " ".join(p)
        lletres = " ".join(f"{subs.get(c, '_'):>2}" for c in p)
        if len(dalt) + len(codis) + 3 > AMPLADA:
            print("  " + dalt)
            print("  " + baix)
            print()
            dalt, baix = "", ""
        dalt += codis + " / "
        baix += lletres + "   "
    if dalt:
        print("  " + dalt)
        print("  " + baix)


def mostrar_subs():
    """Mostra les substitucions actuals agrupades per lletra."""
    if not subs:
        print("\n  (cap substitucio definida)")
        return
    per_lletra = {}
    for codi, lletra in subs.items():
        per_lletra.setdefault(lletra, []).append(codi)
    print("\n  Substitucions actuals:")
    for lletra in sorted(per_lletra):
        print(f"    {' '.join(sorted(per_lletra[lletra]))} -> {lletra}")


def mostrar_progres():
    """Mostra el percentatge de simbols identificats i els codis pendents."""
    coneguts = sum(1 for s in tots_simbols if s in subs)
    pendents = sorted(
        (c for c in comptador if c not in subs),
        key=lambda c: -comptador[c]
    )
    print(f"\n  Identificats: {coneguts}/{total_simbols}"
          f" ({coneguts / total_simbols * 100:.1f}%)")
    print(f"  Codis pendents ({len(pendents)}): {' '.join(pendents)}")


def mostrar_tot():
    """Mostra substitucions + progres + text parcial."""
    mostrar_subs()
    mostrar_progres()
    print("\n  Text parcial:\n")
    if vista_doble:
        mostrar_text_doble()
    else:
        mostrar_text_compacte()
    print()


# ============================================================
#  Modificar hipotesis
# ============================================================

def guardar_snapshot(descripcio):
    """Guarda l'estat actual abans de fer un canvi."""
    historial.append((descripcio, dict(subs)))


def _aplica(assignacions):
    """Aplica una llista de parelles (codi, lletra), en deixa rastre a
    l'historial i avisa de les lletres que es passen de la seva
    frequencia esperada al catala.  Retorna True si hi ha hagut canvis."""
    guardar_snapshot(", ".join(f"{c}->{l}" for c, l in assignacions))

    for c, l in assignacions:
        subs[c] = l

    # per cada lletra tocada, comparem el total del seu grup d'homofons
    # amb el percentatge que hauria de representar al catala
    for lletra in {l for _, l in assignacions}:
        total = sum(comptador[x] for x, l in subs.items() if l == lletra)
        pct = total / total_simbols * 100
        esperat = freq_catala[lletra]
        if pct > 1.6 * esperat + 1:
            print(f"  ATENCIO: {lletra} suma {pct:.1f}% "
                  f"(catala ~ {esperat:.1f}%)")

    return True


def assignar(codis, lletra):
    """Assigna un o mes codis a una mateixa lletra: 09 18 19 E."""
    lletra = lletra.upper()
    if lletra not in freq_catala:
        print("  La lletra ha de ser A-Z.")
        return False

    for c in codis:
        if c not in comptador:
            print(f"  Avis: el codi {c} no apareix al criptograma.")

    return _aplica([(c, lletra) for c in codis])


def assignar_paraula(codis, paraula):
    """Assigna tota una paraula de cop: 19 28 54 ELS.

    Es comprova que el nombre de codis coincideixi amb el nombre de
    lletres i que el mateix codi no rebi dues lletres diferents dins de
    la mateixa paraula. El segon comprovant es pot activar amb una
    paraula com XIFRATS, on el mateix codi ha de representar sempre la
    mateixa lletra."""
    paraula = paraula.upper()
    if len(codis) != len(paraula):
        print(f"  {len(codis)} codis pero '{paraula}' te "
              f"{len(paraula)} lletres: les longituds no coincideixen.")
        return False

    vist = {}
    for c, lletra in zip(codis, paraula):
        if c in vist and vist[c] != lletra:
            print(f"  El codi {c} surt dues vegades amb lletres "
                  f"diferents ({vist[c]} i {lletra}): impossible.")
            return False
        vist[c] = lletra

    nous = {c: l for c, l in vist.items() if subs.get(c) != l}
    if not nous:
        print(f"  '{paraula}' ja est̀a assignada.")
        return False

    for c, lletra in sorted(nous.items()):
        if lletra not in freq_catala:
            print("  La lletra ha de ser A-Z.")
            return False

    return _aplica(sorted(nous.items()))


def eliminar(codi):
    """Elimina la hipotesi d'un codi."""
    if codi not in subs:
        print(f"  No hi ha hipotesi per a {codi}.")
        return False
    lletra = subs[codi]
    guardar_snapshot(f"eliminat {codi}->{lletra}")
    del subs[codi]
    print(f"  Eliminat: {codi} -> {lletra}")
    return True


def desfer():
    """Restaura l'estat anterior."""
    if not historial:
        print("  No hi ha res a desfer.")
        return False
    desc, anterior = historial.pop()
    subs.clear()
    subs.update(anterior)
    print(f"  Desfet: {desc}")
    return True


def reset():
    """Elimina totes les hipotesis."""
    guardar_snapshot("reset")
    subs.clear()


# ============================================================
#  Ajuda
# ============================================================

AJUDA = """
  Comandes disponibles:

  ASSIGNAR (el prefixe "assignar" es opcional)
    28 E              assigna el codi 28 a la lletra E
    09 18 19 E        assigna mes d'un codi a la mateixa lletra (els homofons)
    19 28 54 ELS      assigna tota una paraula de cop: 19->E, 28->L, 54->S
    28 -> E           format amb fletxa (tambe funciona)

  ELIMINAR / DESFER
    del 28            elimina la hipotessi del codi 28
    undo              desfer l'últim canvi
    reset             elimina totes les hipotesis
    historial         llista els canvis fets fins ara

  ANALISI
    freq              frequencia de cada codi i la seva hipotessi
    lletres           frequencia per lletra comparada amb el catala
    paraules N        llista les paraules de N simbols
    context 28        veins de cada aparicio del codi 28
    encaixa PARAULA   paraules del criptograma compatibles amb PARAULA

  VISUALITZACIO
    doble             alterna la vista simple i la doble (codis a dalt,
                      lletres a sota)

  q / sortir          surt del programa

  Exemple de partida:
    > paraules 3
    > 19 28 54 ELS
    > encaixa HOMOFONICS
"""


# ============================================================
#  Bucle principal
# ============================================================

def normalitza_codi(s):
    """Retorna el codi normalitzat a 2 digits, o None si no es numeric."""
    return s.zfill(2) if s.isdigit() else None


def interpretar(entrada):
    """Interpreta una comanda. Retorna False si cal sortir."""
    global vista_doble

    parts = entrada.replace("->", " ").split()
    if not parts:
        return True
    cmd = parts[0].lower()

    # el prefixe "assignar" es opcional: "19 28 54 ELS" i
    # "assignar 19 28 54 ELS" són la mateixa comanda
    if cmd in ("assignar", "posar", "a"):
        parts = parts[1:]
        if not parts:
            print("  Cal indicar els codis i la lletra. Ajuda: 'ajuda'.")
            return True
        cmd = parts[0].lower()

    if cmd in ("q", "sortir", "exit", "quit"):
        return False

    elif cmd in ("ajuda", "help"):
        print(AJUDA)

    elif cmd == "freq":
        freq_codis()

    elif cmd == "lletres":
        freq_lletres()

    elif cmd == "historial":
        if not historial:
            print("  Encara no hi ha canvis.")
        else:
            for i, (desc, _) in enumerate(historial, 1):
                print(f"  {i:>3}. {desc}")

    elif cmd == "paraules" and len(parts) == 2 and parts[1].isdigit():
        llista_paraules(int(parts[1]))

    elif cmd == "context" and len(parts) == 2 and normalitza_codi(parts[1]):
        context_codi(normalitza_codi(parts[1]))

    elif cmd == "encaixa" and len(parts) == 2 and parts[1].isalpha():
        encaixa(parts[1])

    elif cmd == "doble":
        vista_doble = not vista_doble
        mostrar_tot()

    elif cmd == "undo":
        if desfer():
            mostrar_tot()

    elif cmd == "reset":
        reset()
        mostrar_tot()

    elif cmd == "del" and len(parts) == 2 and normalitza_codi(parts[1]):
        if eliminar(normalitza_codi(parts[1])):
            mostrar_tot()



    # Assignacio: un o mes codis seguits d'una lletra
    elif (len(parts) >= 2
          and all(normalitza_codi(p) for p in parts[:-1])
          and parts[-1].isalpha()):
        codis = [normalitza_codi(p) for p in parts[:-1]]
        lletra = parts[-1]
        if len(lletra) == 1:
            assignar(codis, lletra)
        else:
            assignar_paraula(codis, lletra)
        mostrar_tot()

    else:
        print("  Comanda no reconeguda. Escriu 'ajuda'.")

    return True


# --- Inici ---
print("=" * 50)
print("  ASSISTENT DE CRIPTOANALISI")
print("  Substitucio homofonica")
print("=" * 50)
print("  Escriu 'ajuda' per veure les comandes.")
mostrar_tot()

while True:
    try:
        entrada = input("> ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        break
    if not interpretar(entrada):
        break
