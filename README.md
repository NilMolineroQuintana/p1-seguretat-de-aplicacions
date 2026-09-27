# Pràctica 1: Criptografia clàssica
**Grup:** Guillem Alcoverro, Nil Molinero

## Requisits

- Python 3.10 o superior
- No calen dependències externes; tots els scripts fan servir únicament la biblioteca estàndard de Python.

---

## Estructura del projecte

```
.
├── README.md                  # Aquest fitxer
├── informe.md                 # Informe de la pràctica
├── IA.md                      # Ús de la intel·ligència artificial
├── criptogrames/
│   ├── A.txt                  # Criptograma A (substitució monoalfabètica)
│   ├── B.txt                  # Criptograma B (substitució homofònica)
│   ├── C.txt                  # Criptograma C (Vigenère)
│   └── CLASSE.txt             # Criptograma de la competició atacant-defensor
└── codi/
    ├── analitza.py             # Anàlisi estadística de criptogrames
    ├── atac_substitucio.py     # Atac assistit a substitució monoalfabètica
    ├── atac_vigenere.py        # Atac automàtic a Vigenère
    ├── atac_homofonic.py       # Atac assistit a substitució homofònica
    ├── xifrar.py               # Xifratge de Vigenère (fase 4)
    └── frequencies/
        └── catala.csv          # Freqüències de lletres en català
```

---

## Com executar els programes

Totes les comandes s'executen des del directori `codi/`.

### 1. `analitza.py` — Anàlisi estadística d'un criptograma

Calcula longitud, nombre de símbols, freqüències, índex de coincidència, bigrames, trigrames i grams repetits.

```bash
python analitza.py ../criptogrames/A.txt
```

Opcions:

| Argument       | Descripció                                               |
| -------------- | -------------------------------------------------------- |
| `criptograma`  | Ruta al fitxer amb el criptograma (obligatori)           |
| `--max N`      | Mida màxima dels grams a cercar (per defecte 5)          |

Exemples:

```bash
# Analitzar el criptograma B (símbols numèrics)
python analitza.py ../criptogrames/B.txt

# Analitzar el criptograma C amb grams fins a mida 8
python analitza.py --max 8 ../criptogrames/C.txt
```

---

### 2. `atac_substitucio.py` — Atac assistit a una substitució monoalfabètica

Eina interactiva que mostra les freqüències comparades amb el català i permet introduir hipòtesis de substitució una a una, veient immediatament el text parcialment desxifrat.

```bash
python atac_substitucio.py ../criptogrames/A.txt
```

Comandes dins del programa:

| Comanda    | Descripció                                    |
| ---------- | --------------------------------------------- |
| `X Y`      | Substitueix la lletra `X` per `Y`             |
| `-X`       | Elimina la substitució de `X`                 |
| `freq`     | Mostra la taula de freqüències                |
| `q`        | Surt del programa                             |

---

### 3. `atac_vigenere.py` — Atac automàtic a Vigenère

Rep únicament el criptograma i proposa la longitud de la clau (Kasiski + IC), els desplaçaments de cada posició i el text desxifrat.

```bash
python atac_vigenere.py ../criptogrames/C.txt
```

Opcionalment es pot indicar un fitxer CSV de freqüències diferent del català:

```bash
python atac_vigenere.py ../criptogrames/C.txt frequencies/catala.csv
```

---

### 4. `atac_homofonic.py` — Atac assistit a una substitució homofònica

Eina interactiva per atacar criptogrames amb símbols numèrics i separador `/`. Permet assignar codis a lletres, veure el context de cada codi, cercar paraules compatibles, desfer canvis, etc.

```bash
python atac_homofonic.py ../criptogrames/B.txt
```

Comandes principals dins del programa:

| Comanda              | Descripció                                                |
| -------------------- | --------------------------------------------------------- |
| `28 E`               | Assigna el codi `28` a la lletra `E`                     |
| `09 18 19 E`         | Assigna diversos codis a la mateixa lletra (homòfons)     |
| `19 28 54 ELS`       | Assigna tota una paraula de cop                           |
| `del 28`             | Elimina la hipòtesi del codi `28`                         |
| `undo`               | Desfà l'últim canvi                                       |
| `reset`              | Elimina totes les hipòtesis                               |
| `freq`               | Freqüència de cada codi                                   |
| `lletres`            | Freqüència per lletra comparada amb el català             |
| `paraules N`         | Llista les paraules de `N` símbols                        |
| `context 28`         | Veïns de cada aparició del codi `28`                      |
| `encaixa PARAULA`    | Paraules del criptograma compatibles amb `PARAULA`        |
| `doble`              | Alterna vista simple / vista doble (codis + lletres)      |
| `ajuda`              | Mostra totes les comandes disponibles                     |
| `q`                  | Surt del programa                                         |

---

### 5. `xifrar.py` — Xifratge de Vigenère (fase 4)

Script utilitzat per xifrar el text de la competició atacant-defensor amb una clau de Vigenère. Elimina accents, espais i puntuació, xifra el text i verifica que el desxifrat recupera l'original.

```bash
python xifrar.py
```

> **Nota:** la clau i el text estan definits directament dins del fitxer. Per canviar-los, editeu les variables `clau` i `text` al final del script.
