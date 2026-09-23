import unicodedata

def limpiar(texto):
    texto = unicodedata.normalize('NFKD', texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return "".join(c for c in texto if c.isalpha())

def cifrar(texto, clave):
    texto = limpiar(texto).upper()
    resultado = ""
    for i, c in enumerate(texto):
        k = ord(clave[i % len(clave)]) - ord('A')
        resultado += chr((ord(c) - ord('A') + k) % 26 + ord('A'))
    return resultado

def descifrar(texto, clave):
    texto = limpiar(texto).upper()
    resultado = ""
    for i, c in enumerate(texto):
        k = ord(clave[i % len(clave)]) - ord('A')
        resultado += chr((ord(c) - ord('A') - k) % 26 + ord('A'))
    return resultado

def agrupar(texto, n):
    return " ".join(texto[i:i+n] for i in range(0, len(texto), n))

# Ejemplo

gruposde = 8
clave = "PROVA"
texto = "Si esteu llegint aquest text significa que ho heu aconseguit aquest text ha estat redactat pel grup format per Guillem Alcoverro i Nil Molinero per veure si el grup que ho ha de desxifrar ho aconsegueix aquest text estarà xifrat en Vigenère amb una clau definida per nosaltres mateixos us recomanem analitzar bé la freqüència de les lletres i cercar possibles patrons repetits per descobrir la paraula secreta esperem que el grup assignat tingui molta sort i apliqui bones tècniques d'anàlisi i aconsegueixi esbrinar tots els detalls d'aquest tipus de xifratge"

c = cifrar(texto, clave)
print("Cifrado:", agrupar(c, gruposde))
print("Descifrado:", descifrar(c, clave))