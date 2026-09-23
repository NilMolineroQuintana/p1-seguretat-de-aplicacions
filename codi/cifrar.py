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
clave = "PROVA"
texto = "AIXÓ ÉS UNA PROVA"

c = cifrar(texto, clave)
print("Cifrado:", agrupar(c, 5))
print("Descifrado:", descifrar(c, clave))