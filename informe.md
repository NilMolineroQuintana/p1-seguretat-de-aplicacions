# Pràctica 1: Criptografia clàssica
**Grup:** Guillem Alcoverro, Nil Molinero

## Tasca 1

### 1.1. Programa d'anàlisi

Hem preparat `analitza.py`, que rep el criptograma per argument (i opcionalment `--max N`) i calcula: la longitud del criptograma, el nombre de símbols diferents, les freqüències absolutes i relatives de cada símbol, els símbols més freqüents, l'índex de coincidència i les repeticions de bigrames, trigrames i grams més llargs amb les posicions i les distàncies entre ocurrències. Si el criptograma conté nombres (com per exemple el text B.txt), cada nombre es tracta com un símbol; si només conté lletres, cada lletra ho és.

### 1.2 Classificació

#### A.txt

A simple vista i executant el programa d'anàlisi `analitza.py` que hem preparat pensem que pot ser una **substitució monoalfabètica**.

L'índex de coincidència calculat és de `0.0726`, cosa que s'aproxima molt al valor esperat per a un text en català (~0.072–0.078). Si fos un xifratge polialfabètic com Vigenère, l'IC tendria a baixar cap a ~0.038. Això indica que la distribució de freqüències del text original es conserva intacta, fet característic d'una substitució monoalfabètica.

A més, el criptograma conté només `22` símbols diferents d'un alfabet de 26 lletres, i la distribució de freqüències segueix un perfil irregular típic d'un idioma natural: `Z` (12.99%), `T` (12.06%), `I` (8.35%), `R` (8.12%). Aquestes freqüències encaixen amb les lletres més comunes del català segons la taula que utilitzem (`E` 16.01%, `A` 14.47%, `S` 7.43%, `T` 5.44%): `Z`→`E`, `T`→`A`, `I`→`S` i `R`→`T`. El bigrama `ZI` apareix 13 vegades, cosa que reforça que es tracta de patrons lingüístics preservats per la substitució. També observem que els espais entre paraules es mantenen intactes i hi ha paraules curtes repetides (`ZY`, `FY`, `ZO`, `PZ`) que probablement corresponen a articles i preposicions del català.

En aquest cas pensem que l'atac més adient per a desxifrar aquest text serà basar-nos en l'anàlisi de freqüències i comparar-lo directament amb les freqüències de lletres més comunes en català, mirant bigrames, trigrames, paraules curtes, i poc a poc anar deduint les substitucions fins a resoldre el xifratge.

#### B.txt

En executar `analitza.py` veiem que el criptograma fa servir `58` símbols diferents, tots ells codis numèrics de dos dígits, i les paraules estan separades pel caràcter `/`. Com que l'alfabet del català només té `26` lletres, una substitució monoalfabètica simple és impossible: cal que dos o més codis diferents representin la mateixa lletra. A més l'IC sembla massa baix per a ser Vigenere per tant creiem que és un text xifrat amb una **substitució homofónica**.

L'índex de coincidència dels `58` símbols és de `0.0189`, pràcticament el valor aleatori per a un alfabet d'aquesta mida i molt lluny del `0.073` esperat per al català. Si fos una substitució monoalfabètica (26 símbols), l'IC conservaria el perfil del llenguatge original; el fet que caigui fins al nivell aleatori confirma que cada lletra s'ha repartit entre diversos codis, aplanant completament la distribució de freqüències.

A més, l'histograma de símbols és gairebé pla: el codi més freqüent (`10`) apareix `13` vegades (`4.32%`) i el menys freqüent (`25`) només `1` vegada (`0.33%`), amb una diferència entre el màxim i el mínim de menys de `4` punts percentuals. En una substitució monoalfabètica com la del criptograma A, la lletra més freqüent (`Z`) representava el `12.99%` i la menys freqüent no arribava a l'`1%`, un rang molt més ampli que permetia comparar directament amb les freqüències del català. Aquí, en canvi, cap codi destaca prou perquè un atac de freqüències individuals sigui viable; cal aprofitar la informació lingüística que el xifratge no ha esborrat, com la longitud de cada paraula (els `/` separen paraules), les paraules curtes, els patrons de repetició de bigrames (per exemple `56 11` apareix `4` vegades) i la coherència del text parcialment desxifrat.

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

>LA CRIPTOGRAFIA CLÀSSICA ENS ENSENYA UNA LLIÇÓ IMPORTANT UN ESPAI DE CLAUS MOLT GRAN NO GARANTEIX SEGURETAT SI EL XIFRATGE CONSERVA PROU ESTRUCTURA DEL LLENGUATGE UN ATACANT POT EXPLOTAR LES REGULARITATS ESTADÍSTIQUES EN UNA SUBSTITUCIÓ MONOALFABÈTICA PER EXEMPLE CADA LLETRA DEL TEXT ORIGINAL ES TRANSFORMA SEMPRE EN EL MATEIX SÍMBOL AIXÒ CONSERVA LES FREQÜÈNCIES ELS PATRONS I MOLTES DEPENDÈNCIES ENTRE LLETRES UN BON CRIPTOANALISTA NO BUSCA NOMÉS LA CLAU BUSCA INFORMACIÓ QUE EL SISTEMA HA DEIXAT ESCAPAR


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

>QUAN UN XIFRAT POLIALFABÈTIC UTILITZA UNA CLAU PERIÒDICA, LA DISTRIBUCIÓ GLOBAL DE FREQÜÈNCIES ES POT APROPAR MOLT MÉS A UNA DISTRIBUCIÓ UNIFORME. AIXÒ FA QUE L'ANÀLISI DIRECTA SIGUI MENYS EFICAÇ. PERÒ LA PERIODICITAT DE LA CLAU INTRODUEIX UNA NOVA REGULARITAT: SI SEPAREM LES POSICIONS DEL CRIPTOGRAMA SEGONS LA SEVA POSICIÓ MÒDUL LA LONGITUD DE LA CLAU, CADA SUBSEQÜÈNCIA ES COMPORTA COM UN XIFRAT DE CÈSAR. AQUESTA IDEA PERMET COMBINAR KASISKI, ÍNDEX DE COINCIDÈNCIA I ANÀLISI DE FREQÜÈNCIES PER RECUPERAR LA CLAU.

L'atac és gairebé automàtic: només cal passar-li el criptograma i el programa proposa la longitud, la clau i restitueix les `428` lletres del text. L'única part que requereix interpretació humana és validar la clau candidata escollida entre les alternatives mostrades. El text s'ha presentat més amunt reintroduint a mà espais, accents i puntuació perquè es pugui llegir; el programa retorna només lletres seguides.

### 2.3 Atac al criptograma B

Hem implementat `atac_homofonic.py`, una eina d'atac manual molt semblant a la que vam fer servir per al criptograma A però adaptada per a símbols numèrics. El script està basat en un programa del nostre company Asier que hem adaptat i integrat al nostre flux de treball.

Com hem explicat a la classificació, un atac basat únicament en les freqüències individuals dels símbols no funciona aquí: l'histograma és gairebé pla perquè cada lletra es reparteix entre diversos codis, de manera que cap codi destaca prou per poder-lo assignar directament a una lletra freqüent del català. Ara bé, el xifratge homofònic no esborra tota l'estructura del llenguatge: els separadors `/` conserven els límits entre paraules i, per tant, les longitudes de cada paraula i els patrons de repetició es mantenen intactes.

Vam començar per les paraules més curtes del criptograma i anar avançant cap a les més llargues per facilitar-nos la feina: una paraula d'un sol símbol té molt poques candidates en català (articles o preposicions com "A", "I", "O"), i una de tres en té moltes més però encara asequibles. La primera paraula, `19 28 54`, consta de tres símbols. En català, una paraula de tres lletres molt habitual al principi d'una frase és "ELS", així que vam provar `19→E`, `28→L` i `54→S`. Amb aquestes tres substitucions, altres fragments del text parcialment desxifrat ja van començar a tenir sentit, i vam anar estenent les hipòtesis: `51→D` per completar paraules que semblaven "DEL" o "DE", `09→E` i `44→L` com a segons homòfons d'E i L respectivament.

A diferència de l'atac al criptograma A, aquí vam cometre un error de bloc important. Després de les primeres substitucions vam intentar assignar ràpidament diversos codis: `36→Q`, `37→U`, `05→U`, `56→E`, `11→L`, `60→L`, `59→N`, `49→A` i `10→A`. Cap d'aquestes hipòtesis produïa fragments coherents, i el text parcial no s'assemblava a cap frase en català, de manera que vam haver d'eliminar les nou substitucions i tornar enrere.

Una vegada revertits aquests canvis vam reprendre l'atac de forma més prudent. Primer vam fixar els codis de les lletres més freqüents a partir del context: `62→D`, `42→E`, `10→S`, `46→E`, `39→N`, `07→A`, `12→T`. A continuació, el símbol `49` ens va donar problemes: vam provar primer `49→N`, després `49→A`, i finalment `49→S` va ser l'única opció que feia que paraules com "DIVERSOS" i "SIMBOLS" tinguessin sentit. Amb prou lletres ja visibles, la resta de substitucions les vam deduir pel context de les paraules parcialment desxifrades: `36→I`, `37→M`, `56→B`, `11→O`, i així fins a completar les `58` assignacions.

En total, l'atac ha requerit `85` accions (substitucions i eliminacions). La clau de l'èxit no ha estat l'anàlisi de freqüències que aquí es molt poc efectiu, sinó la combinació de la longitud de les paraules, els patrons de repetició i la coherència lingüística del text parcialment desxifrat. El text original recuperat és:

>ELS XIFRATS HOMOFONICS INTENTEN DIFICULTAR L'ANALISI DE FREQUENCIES ASSIGNANT DIVERSOS SIMBOLS A LES LLETRES MES HABITUALS SI LA TRIA DEL SIMBOL ES PROU ALEATORIA LES FREQUENCIES DELS SIMBOLS INDIVIDUALS PODEN QUEDAR MOLT MES REPARTIDES AIXO NO ELIMINA TOTA L'ESTRUCTURA DEL LLENGUATGE PERO OBLIGA L'ATACANT A BUSCAR RELACIONS MES RIQUES ENTRE ELS SIMBOLS

## Tasca 3: Auditoria d'un programa generat per IA

Hem auditat el programa d'atac automàtic a Vigenère proposat per la intel·ligència artificial. El codi original s'ha guardat a `codi/original_ia.py` i la versió corregida a `codi/corregit_ia.py`.

### 3.1 Entendre abans de jutjar

El programa de la IA divideix l'atac en set funcions:

1. **`neteja(text)`**: Filtra caràcters no alfabètics i passa a majúscules. Assumeix un text format únicament per les 26 lletres de l'alfabet anglès (A–Z).
2. **`index_coincidencia(text)`**: Calcula l'IC ($\frac{\sum f_i(f_i-1)}{n(n-1)}$). Es basa en el fet que un text monoalfabètic en llenguatge natural té un IC alt (~0.07 pel català) a causa dels pics de freqüència, mentre que un text polialfabètic s'aplana cap a la distribució uniforme (~0.038).
3. **`longitud_clau(text, maxim=20)`**: Divideix el text en $k$ columnes (`text[i::k]`) i tria el $k$ amb major IC mitjà. Assumeix que quan $k$ és la longitud de la clau, cada columna esdevé un xifratge monoalfabètic de Cèsar i el seu IC assoleix el valor del llenguatge natural.
4. **`desplacament_columna(col)`**: Extreu el caràcter més comú de la columna i en calcula la distància a la 'E'. Assumeix cegament que la lletra més freqüent de qualsevol columna monoalfabètica és sempre la 'E'.
5. **`troba_clau(text, k)`**: Aplica `desplacament_columna` a cadascuna de les $k$ columnes per separat, assumint que cada component de la clau es pot resoldre de forma aïllada.
6. **`desxifra(text, clau)`**: Aplica la resta modular $m_i = (c_i - k_i) \pmod{26}$, implementant el desxifrat clàssic de Vigenère.
7. **`ataca(text)`**: Enllaça tot el flux assumint que l'atac pot ser 100% autònom sense necessitat d'intervenció humana ni ajust lingüístic.

### 3.2 Buscar problemes

Hem identificat tres problemes greus en el codi de la IA:

#### 1. Fallada durant l'execució (Crash per `ZeroDivisionError` i `IndexError`)
A `index_coincidencia`, el denominador `n * (n - 1)` dóna zero si $n \le 1$. Com que `longitud_clau` itera fixament fins a $k=20$, qualsevol text de menys de 40 caràcters genera columnes de longitud 0 o 1 i fa fallar el programa amb una divisió per zero:
```python
ataca("HOLA")  # ZeroDivisionError: division by zero
```
A més, si una columna és buida, `Counter(col).most_common(1)[0][0]` a `desplacament_columna` genera un `IndexError`.

#### 2. Resposta incorrecta (Heurística de la lletra 'E')
Assumir que la lletra més freqüent de cada columna és sempre la 'E' és fals en textos reals, on lletres com la 'A', 'S' o 'T' sovint la superen (en català, 'A' té un 14.5% i 'E' un 16.0%).
En passar el **Criptograma C** per `original_ia.py`, el programa detecta $k=7$ però obté la clau errònia **`ISJTWAM`** en lloc de **`MONTSEC`** (només encerta la 'T'). Com a resultat, el text desxifrat és completament il·legible (`UQENQRNMBV...`).

#### 3. Resposta aparentment raonable però injustificada (Tria de múltiples de clau)
`longitud_clau` fa `if ic_mitja > millor_ic`. Com que qualsevol múltiple de la clau ($2k, 3k, \dots$) també forma columnes monoalfabètiques, la variància mostral en columnes més curtes fa que sovint un múltiple assoleixi un IC lleugerament superior per pur atzar.
Per exemple, si una clau real té longitud 7 (com a `MONTSEC`) i per soroll estadístic s'obté $IC(7) = 0.0696$ i $IC(14) = 0.0710$, el programa de la IA tria automàticament **$k = 14$** només perquè té un IC més alt. Aquesta conclusió sembla raonable pel valor elevat de l'IC, però és injustificada: duplica innecessàriament la clau i divideix la mostra per la meitat en lloc d'escollir el període fonamental $k = 7$.

### 3.3 Corregir-lo

Hem implementat la versió corregida a `codi/corregit_ia.py` aplicant tres millores:

1. **Robustesa:** A `index_coincidencia`, si $n < 2$ retornem `0.0`. A `longitud_clau`, limitem la cerca a $maxim = \min(maxim, \lfloor n/2 \rfloor)$ i calculem la mitjana ignorant columnes amb menys de 2 caràcters.
2. **Període fonamental:** Entre els candidats amb $IC \ge 0.055$, triem el $k$ més petit que assoleixi com a mínim el 85% de l'IC màxim trobat.
3. **Comparació completa de freqüències:** A `desplacament_columna`, carreguem `frequencies/catala.csv` i provem els 26 desplaçaments, triant el que minimitza la suma de diferències absolutes respecte a la distribució real del català en lloc de mirar només la 'E'.

Amb aquests canvis, `corregit_ia.py` no falla amb textos curts, identifica sempre el període fonamental evitant múltiples espuris, i recupera exactament la clau `MONTSEC` i el text clar del Criptograma C.

### 3.4 Pregunta final

> **Suposeu que el programa obté:**
> ```
> IC (7) = 0.0696
> IC (14) = 0.0710
> ```
> **El programa retorna automàticament `k = 14`. És correcta aquesta conclusió? Expliqueu com comprovaríeu si la clau té realment longitud 14 o si té un període fonamental més curt.**

**No, la conclusió no és correcta.**

Si una clau té longitud 7, les columnes a pas 14 també estan formades per lletres xifrades amb el mateix desplaçament ($i \equiv i+14 \pmod 7$). Per tant, el seu IC teòric també és el d'un text monoalfabètic (~0.07). La lleugera diferència entre 0.0696 i 0.0710 és pur soroll estadístic degut a tenir columnes amb la meitat de lletres. Triar $k=14$ és un sobreajust injustificat; cal buscar sempre el **període fonamental**.

Per comprovar si la clau és de període 7 o 14:
1. **Inspecció de la clau:** Si en desxifrar amb $k=14$ la clau té la forma $K_0 \dots K_6 K_0 \dots K_6$ (es repeteix a la segona meitat), el període real és clarament 7.
2. **Kasiski:** Si entre les distàncies de patrons repetits hi ha múltiples senars de 7 (com 21, 35, 49...), la longitud no pot ser 14, ja que aquestes distàncies no són divisibles per 14.
3. **IC creuat:** Calcular l'IC mutu entre la columna $i$ i la columna $i+7$. Si és alt (~0.07), totes dues comparteixen el mateix desplaçament i el període és 7.
4. **Coherència lingüística:** Avaluar si la clau de 7 lletres forma una paraula amb sentit (com `MONTSEC`), mentre que duplicar-la no afegeix informació.

## Tasca 4

### 4.1 Construcció del repte

Hem redactat un text original de `91` paraules, que usant `xifrar.py` hem xifrat amb la clau `CRIPTOGRAFIA`.

El programa `xifrar.py` elimina accents, espais i signes de puntuació abans de xifrar, com exigeix la modalitat B, mostra el text xifrat en grups de 8 lletres i comprova automàticament que el desxifrat recupera el text original.

El nostre text original era el següent:

>Si esteu llegint aquest text significa que ho heu aconseguit aquest text ha estat redactat pel grup format per Guillem Alcoverro i Nil Molinero per veure si el grup que ho ha de desxifrar ho aconsegueix aquest text estara xifrat en Vigenere amb una clau definida per nosaltres mateixos us recomanem analitzar be la frequencia de les lletres i cercar possibles patrons repetits per descobrir la paraula secreta esperem que el grup assignat tingui molta sort i apliqui bones tecniques d'analisi i aconsegueixi esbrinar tots els detalls d'aquest tipus de xifratge

### 4.2 L'atac

El text xifrat que ens ha proporcionat és del grup format per:
- Aleix Ràfols
- Samuel Gumà

El criptograma es troba dins de `CLASSE.txt`. En primer lloc, vam passar-lo pel nostre script d'anàlisi i vam observar que l'índex de coincidència era de `0.0429`, valor clarament allunyat del IC del català i proper al valor aleatori, cosa que indicava un xifratge polialfabètic. A més, el nombre de caràcters únics del criptograma era exactament `26` i l'histograma de freqüències presentava una distribució força aplanada, sense els pics característics d'una substitució monoalfabètica. Tot plegat ens va fer deduir que es tractava d'un xifratge de Vigenère.

Vam executar `atac_vigenere.py` amb el criptograma com a argument, però el resultat va ser un text inintel·ligible amb la clau `KUMAN`. En examinar les estadístiques generades pel propi atac, vam observar que els períodes candidats eren tots múltiples de `5`. El nostre codi original triava sempre el menor dels candidats, tot i que l'IC no s'aproximés prou al del català. Vam provar aleshores amb longitud `10`, que era la que presentava un IC més proper al català, i efectivament el programa va recuperar la clau correcta i el text completament desxifrat. Arran d'això, vam modificar el codi d'atac per tal que seleccioni com a longitud candidata la que té l'IC més semblant al del català, en lloc de la mínima.

La clau era `TUTANKAMON` i el text desxifrat aquest:

>LA TARDOR PORTA DIES CURTS I FREDS A LA PLAÇA DEL POBLE ELS NENS JUGUEN SENSE PARAR FINS QUE ES FA FOSC JUGANT AMB CINC XIQUES I FENT BROMES EL PALLASSO DE VIC PERD LA QUALITAT DEL XOU LES FAMILIES SURTEN A PASSEJAR PEL PARC I COMPREN PA CALENTA LA FLECA DEL CANTO LA NOSTRA AVIA FA SOPA DE VERDURES MENTRES ESCOLTA LA RADIO I FIX VICTOR PUJA DALT I QUAN SES FONDRA EL LLARG CAMI TROBA PERLES I JOIES DEMA SERA UN ALTRE DIA TRANQUIL I PLE DE PETITES ALEGRIES QUOTIDIAN ESPERA TOTHOM

## Conclusions

Al llarg d'aquesta pràctica hem pogut estudiar empíricament com la criptografia clàssica es fonamenta en la lluita per amagar les regularitats estructurals i estadístiques del llenguatge:

1. **Substitució monoalfabètica:** Tot i comptar amb un espai de claus enorme ($26! \approx 4 \times 10^{26}$) que fa impossible la força bruta, conserva íntegrament la distribució de freqüències i patrons del llenguatge d'origen. Això la fa immediatament vulnerable a l'anàlisi de freqüències i paraules curtes.
2. **Substitució homofònica:** Repartir les lletres més freqüents entre diversos símbols aconsegueix aplanar l'histograma individual i baixar l'índex de coincidència. No obstant això, si es conserven els separadors de paraula, l'estructura sintàctica (longituds, patrons de repetició de bigrames i coherència lèxica) continua viva i permet recuperar el text de forma assistida.
3. **Xifratge polialfabètic (Vigenère):** Difumina les freqüències globals acostant-les a una distribució uniforme, però la repetició periòdica de la clau introdueix una vulnerabilitat fatal: les posicions congruents mòdul la longitud de la clau esdevenen xifrats de Cèsar independents, explotables mitjançant Kasiski, l'índex de coincidència i la correlació de freqüències.
4. **Auditoria d'eines automàtiques i ús de la IA:** Hem comprovat que un codi generat per IA que aparenta ser funcional pot contenir errors greus de disseny si es basa en simplificacions excessives (com suposar que la lletra més freqüent sempre és la 'E' o triar cegament el màxim d'IC ignorant el període fonamental). El coneixement teòric i la capacitat d'auditoria són imprescindibles per desenvolupar eines criptoanalítiques fiables i robustes.
