import unicodedata

def netejar(text):
    text = unicodedata.normalize('NFKD', text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return "".join(c for c in text if c.isalpha())

def xifrar(text, clau):
    text = netejar(text).upper()
    resultat = ""
    for i, c in enumerate(text):
        k = ord(clau[i % len(clau)]) - ord('A')
        resultat += chr((ord(c) - ord('A') + k) % 26 + ord('A'))
    return resultat

def desxifrar(text, clau):
    text = netejar(text).upper()
    resultat = ""
    for i, c in enumerate(text):
        k = ord(clau[i % len(clau)]) - ord('A')
        resultat += chr((ord(c) - ord('A') - k) % 26 + ord('A'))
    return resultat

def agrupar(text, n):
    return " ".join(text[i:i+n] for i in range(0, len(text), n))

# Exemple

mida_grup = 8
clau = "CRIPTOGRAFIA"
text = "Si esteu llegint aquest text significa que ho heu aconseguit aquest text ha estat redactat pel grup format per Guillem Alcoverro i Nil Molinero per veure si el grup que ho ha de desxifrar ho aconsegueix aquest text estara xifrat en Vigenere amb una clau definida per nosaltres mateixos us recomanem analitzar be la frequencia de les lletres i cercar possibles patrons repetits per descobrir la paraula secreta esperem que el grup assignat tingui molta sort i apliqui bones tecniques d'analisi i aconsegueixi esbrinar tots els detalls d'aquest tipus de xifratge"

c = xifrar(text, clau)
print("Xifrat:", agrupar(c, mida_grup))
assert desxifrar(c, clau) == netejar(text).upper(), "El desxifrat no recupera el text original"
print("Desxifrat:", desxifrar(c, clau))