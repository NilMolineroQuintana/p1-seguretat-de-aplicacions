# Pràctica 1
## Grup: Guillem Alcoverro, Nil Molinero

---

## Tasca 1

### 1.1. Programa d'anàlisi

Hem preparat `analitza.py`, que rep el criptograma per argument (i opcionalment `--max N`) i calcula: la longitud del criptograma, el nombre de símbols diferents, les freqüències absolutes i relatives de cada símbol, els símbols més freqüents, l'índex de coincidència i les repeticions de bigrames, trigrames i grams més llargs amb les posicions i les distàncies entre ocurrències. Si el criptograma conté nombres (el B), cada nombre es tracta com un símbol; si només conté lletres, cada lletra ho és.

### 1.2 Classificació

#### A.txt

A simple vista i executant el programa d'anàlisi `analitza.py` que hem preparat pensem que pot ser una substitució monoalfabètica.

L'índex de coincidència calculat és de `0.0726`, cosa que s'aproxima molt al valor esperat per a un text en català (~0.072–0.078). Si fos un xifratge polialfabètic com Vigenère, l'IC tendria a baixar cap a ~0.038. Això indica que la distribució de freqüències del text original es conserva intacta, fet característic d'una substitució monoalfabètica.

A més, el criptograma conté només `22` símbols diferents d'un alfabet de 26 lletres, i la distribució de freqüències segueix un perfil irregular típic d'un idioma natural: `Z` (12.99%), `T` (12.06%), `I` (8.35%), `R` (8.12%). Aquestes freqüències encaixen amb les lletres més comunes del català segons la taula que utilitzem (`E` 16.01%, `A` 14.47%, `S` 7.43%, `T` 5.44%): `Z`→`E`, `T`→`A`, `I`→`S` i `R`→`T`. El bigrama `ZI` apareix 13 vegades, cosa que reforça que es tracta de patrons lingüístics preservats per la substitució. També observem que els espais entre paraules es mantenen intactes i hi ha paraules curtes repetides (`ZY`, `FY`, `ZO`, `PZ`) que probablement corresponen a articles i preposicions del català.

En aquest cas pensem que l'atac més adient per a desxifrar aquest text serà basar-nos en l'anàlisi de freqüències i comparar-lo directament amb les freqüències de lletres més comunes en català, mirant bigrames, trigrames, paraules curtes, i poc a poc anar deduint les substitucions fins a resoldre el xifratge.

#### B.txt

#### C.txt

El criptograma té una longitud de `428` lletres i només fa servir les `26` lletres de l'alfabet (els espais que el separen cada cinc caràcters només ajuden a la lectura i no formen part del xifrat). L'índex de coincidència global és de `0.0411`, molt proper al valor aleatori (`1/26 ≈ 0.038`) i lluny de l'IC del català (≈ `0.07`), cosa que descarta un xifratge monoalfabètic.

L'evidència clau ve de calcular l'IC mitjà de les columnes per a cada possible longitud de clau: per a `k = 7` l'IC puja a `0.0696`, valor típic d'un text en català, mentre que per a la resta de períodes es queda al voltant de `0.04`. Això indica que les posicions separades 7 en 7 comparteixen un mateix xifratge de Cèsar, fet característic de Vigenère. L'IC per a `k = 14` també és alt (`0.0673`), però com que `14 = 2 × 7` és un múltiple, apunta al període fonamental `7` i no a una clau de longitud 14.

L'estratègia d'atac serà combinar Kasiski i l'índex de coincidència per determinar la longitud de la clau, separar el text en subseqüències segons la posició mòdul la longitud, analitzar-ne cada una com un xifratge de Cèsar comparant amb les freqüències del català i, finalment, reconstruir clau i text.

## Tasca 2

### 2.1 Atac assistit a una substitució

El nostre programa `atac_substitucio.py` mostra una taula comparativa de freqüències entre el criptograma i el català, permet introduir substitucions una a una i mostra el text parcialment desxifrat després de cada canvi. Tal com demanava l'enunciat, l'atac és assistit i no completament automàtic: l'objectiu era construir una eina que ajudés el criptoanalista a formular i comprovar hipòtesis.

Vam començar comparant les freqüències del criptograma amb les del català. Les dues lletres més freqüents, `Z` (12.99%) i `T` (12.06%), encaixaven clarament amb `E` (16.01%) i `A` (14.47%), així que van ser les primeres substitucions. A partir d'aquí, les paraules curtes ens van guiar: `OT` → "LA" ens va donar `O→L`, `_el` → "DEL" ens va donar `P→D`, i `_ada` → "CADA" ens va confirmar `V→C`.

Amb aquestes primeres substitucions ja podíem reconèixer fragments del text, i poc a poc vam anar deduint la resta de lletres pel context de les paraules parcialment desxifrades: `F→U` per "UNA" i "CLAUS", `Y→N` per "ENS" i "ENSENYA", i així successivament fins a completar les 22 substitucions.

Però no totes les hipòtesis van ser correctes a la primera. El símbol `I` era el tercer més freqüent del criptograma (8.35%) i, segons les freqüències del català, podia correspondre tant a `S` com a `R`; vam provar primer `I→R`. El trigrama repetit `ZYI` quedava com "ENR" i la paraula `VOTIIUVT` com "CLARRICA", cap dels dos amb aspecte de català. En canvi, amb `I→S` aquestes mateixes paraules es convertien en "ENS" i "CLASSICA", paraules reals i coherents amb el context. Veure el text parcial actualitzat després de cada canvi va fer tant trivial detectar l'error com validar la correcció. El text final recuperat és:

```
LA CRIPTOGRAFIA CLASSICA ENS ENSENYA UNA LLICO IMPORTANT
UN ESPAI DE CLAUS MOLT GRAN NO GARANTEIX SEGURETAT SI EL
XIFRATGE CONSERVA PROU ESTRUCTURA DEL LLENGUATGE UN
ATACANT POT EXPLOTAR LES REGULARITATS ESTADISTIQUES EN
UNA SUBSTITUCIO MONOALFABETICA PER EXEMPLE CADA LLETRA
DEL TEXT ORIGINAL ES TRANSFORMA SEMPRE EN EL MATEIX
SIMBOL AIXO CONSERVA LES FREQUENCIES ELS PATRONS I
MOLTES DEPENDENCIES ENTRE LLETRES UN BON CRIPTOANALISTA
NO BUSCA NOMES LA CLAU BUSCA INFORMACIO QUE EL SISTEMA
HA DEIXAT ESCAPAR
```

### 2.2 Atac al criptograma C

Hem implementat l'atac a `atac_vigenere.py`, que rep únicament el criptograma per argument. Primer determinem la longitud de la clau amb tres indicadors complementaris:

- **Kasiski:** el programa busca trigrames repetits, calcula les distàncies entre ocurrències i n'obté els divisors compatibles. Al criptograma C detecta `34` distàncies amb mcd = `1` (poc informatiu per si sol), però entre els divisors compatibles hi apareixen `7` i `14`, coherents amb un període `7`.
- **Índex de coincidència:** per a cada `k` d'1 a 20 es calcula l'IC mitjà de les `k` columnes. Quan `k` coincideix amb la longitud real de la clau, cada columna es comporta com un xifratge de Cèsar i l'IC s'aproxima al del català (≈ `0.07`); en canvi, per a valors incorrectes es manté a prop del valor aleatori (≈ `0.038`).

Al criptograma C, per a `k = 7` l'IC mitjà és `0.0696` i per a `k = 14` és `0.0673`; tots dos superen el llindar de candidatura. Com que `14 = 2 × 7`, la segona candidatura és un múltiple de la primera: el programa no es limita a prendre el màxim de l'IC, sinó que entre les candidates escull la més petita amb un IC ≥ 85 % del màxim, que és el **període fonamental**; en aquest cas, `7`, tal com exigeix l'enunciat.

Amb la longitud fixada, separem el text en 7 columnes i analitzem cada una com un xifratge de Cèsar independent: provem els 26 desplaçaments i escollim el que millor fa coincidir les freqüències de la columna desxifrada amb les freqüències reals del català (provinents de `frequencies/catala.csv`), minimitzant la suma de diferències absolutes entre les dues distribucions. Això recupera la clau:

```
Clau candidata: MONTSEC
```

Els desplaçaments triats per a cada posició (`M`, `O`, `N`, `T`, `S`, `E`, `C`) tenen una diferència de freqüències clarament inferior a la de les alternatives, cosa que confirma la clau. El text original recuperat és:

> QUAN UN XIFRAT POLIALFABÈTIC UTILITZA UNA CLAU PERIÒDICA, LA DISTRIBUCIÓ GLOBAL DE FREQÜÈNCIES ES POT APROPAR MOLT MÉS A UNA DISTRIBUCIÓ UNIFORME. AIXÒ FA QUE L'ANÀLISI DIRECTA SIGUI MENYS EFICAÇ. PERÒ LA PERIODICITAT DE LA CLAU INTRODUEIX UNA NOVA REGULARITAT: SI SEPAREM LES POSICIONS DEL CRIPTOGRAMA SEGONS LA SEVA POSICIÓ MÒDUL LA LONGITUD DE LA CLAU, CADA SUBSEQÜÈNCIA ES COMPORTA COM UN XIFRAT DE CÈSAR. AQUESTA IDEA PERMET COMBINAR KASISKI, ÍNDEX DE COINCIDÈNCIA I ANÀLISI DE FREQÜÈNCIES PER RECUPERAR LA CLAU.

L'atac és gairebé automàtic: només cal passar-li el criptograma i el programa proposa la longitud, la clau i restitueix les `428` lletres del text. L'única part que requereix interpretació humana és validar la clau candidata escollida entre les alternatives mostrades. El text s'ha presentat més amunt reintroduint a mà espais, accents i puntuació perquè es pugui llegir; el programa retorna només lletres seguides.

## Tasca 3

## Tasca 4

### 4.1 Construcció del repte

Hem redactat un text original de `91` paraules, que usant `xifrar.py` hem xifrat amb la clau `CRIPTOGRAFIA`.

El programa `xifrar.py` elimina accents, espais i signes de puntuació abans de xifrar, com exigeix la modalitat B, mostra el text xifrat en grups de 8 lletres i comprova automàticament que el desxifrat recupera el text original.

### 4.2 L'atac