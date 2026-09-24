# Ús de la intel·ligència artificial

## 1. Per a què l'hem utilitzada

Hem usat l'IA en diferents programes del lliurament i en la redacció de l'informe: per estructurar el codi, depurar-lo, fer-lo més robust a partir de les nostres versions inicials i revisar-ne el disseny.

## 2. Fragment acceptat

La correcció de la funció que escull la longitud de clau a `atac_vigenere.py`, perquè triï la més petita amb IC ≥ 85 % del màxim en lloc del "període fonamental" més petit:

```python
def tria_periode_fonamental(candidats, ics):
    if not candidats:
        return None
    millor = max(candidats, key=lambda k: ics[k])
    llindar = 0.85 * ics[millor]
    grans = sorted(k for k in candidats if ics[k] >= llindar)
    return grans[0]
```

## 3. Propostes descartades o corregides

- Vam descartar una proposta que afegia una cerca local amb una llista de paraules catalanes predefinides per validar la clau: afegia massa codi i depenia de paraules fixades, quan el problema es va resoldre amb una millor selecció del període.
Vam haver de corregir un problema de fase a un criptograma: li faltava un fragment de text xifrat i per això desxifrar directament amb la clau coneguda no funcionava fins que vam completar el fragment.

## 4. Com hem comprovat que el programa funciona

Verificació per re-xifrat: desxifrar amb la clau obtinguda i tornar-la a xifrar reproduïa exactament el criptograma original. A més, els textos resultants eren català coherent, amb l'IC per columnes que confirmava la longitud de la clau, i a `xifrar.py` hi ha una asserció que comprova automàticament que desxifrar recupera el text d'origen.