# Practica 1
## Grup: Guillem Alcoverro, Nil Molinero

---

## Tasca 1

### 1.2 Classificació

#### A.txt

A simple vista i executant el programa d'anàlisi que hem preparat pensem que pot ser una substitució monoalfabètica.

L'índex de coincidència calculat és de `0.0726`, cosa que s'aproxima molt al valor esperat per a un text en català (~0.072–0.078). Si fos un xifratge polialfabètic com Vigenère, l'IC tendria a baixar cap a ~0.038. Això indica que la distribució de freqüències del text original es conserva intacta, fet característic d'una substitució monoalfabètica.

A més, el criptograma conté només `22` símbols diferents d'un alfabet de 26 lletres, i la distribució de freqüències segueix un perfil irregular típic d'un idioma natural: `Z` (12.99%), `T` (12.06%), `I` (8.35%), `R` (8.12%). Aquestes freqüències encaixen amb les lletres més comunes del català (`E` ~13%, `A` ~12%, `S` ~8%, `R` ~7%). El bigrama `ZI` apareix 13 vegades, cosa que reforça que es tracta de patrons lingüístics preservats per la substitució. També observem que els espais entre paraules es mantenen intactes i hi ha paraules curtes repetides (`ZY`, `FY`, `ZO`, `PZ`) que probablement corresponen a articles i preposicions del català.

En aquest cas pensem que l'atac més adient per a desxifrar aquest text serà basar-nos en l'anàlisi de freqüències i comparar-lo directament amb les freqüències de lletres més comunes en català, mirant bigrames, trigrames, paraules curtes, i poc a poc anar deduint les substitucions fins a resoldre el xifratge.

#### B.txt

#### C.txt

## Tasca 2

### 2.1 Atac assistit a una substitució

El nostre programa `atac_substitucio.py` mostra una taula comparativa de freqüències entre el criptograma i el català, permet introduir substitucions una a una i mostra el text parcialment desxifrat després de cada canvi. Tal com demanava l'enunciat, l'atac és assistit i no completament automàtic: l'objectiu era construir una eina que ajudés el criptoanalista a formular i comprovar hipòtesis.

Vam començar comparant les freqüències del criptograma amb les del català. Les dues lletres més freqüents, `Z` (12.99%) i `T` (12.06%), encaixaven clarament amb `E` (16.01%) i `A` (14.47%), així que van ser les primeres substitucions. A partir d'aquí, les paraules curtes ens van guiar: `OT` → "LA" ens va donar `O→L`, `_el` → "DEL" ens va donar `P→D`, i `_ada` → "CADA" ens va confirmar `V→C`.

Amb aquestes primeres substitucions ja podíem reconèixer fragments del text, i poc a poc vam anar deduint la resta de lletres pel context de les paraules parcialment desxifrades: `F→U` per "UNA" i "CLAUS", `I→S` per "CLASSICA", `Y→N` per "ENS" i "ENSENYA", i així successivament fins a completar les 22 substitucions.

Durant el procés no vam tenir cap hipòtesi clarament incorrecta, tot i que en algun moment vam dubtar entre lletres de freqüència similar. El fet de veure el text parcial en temps real ens permetia validar ràpidament cada hipòtesi. El text final recuperat és:

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

## Tasca 3

## Tasca 4