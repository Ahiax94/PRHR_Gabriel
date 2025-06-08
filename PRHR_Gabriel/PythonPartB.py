import re

# === Official control letters ===
LETRAS_CONTROL = "TRWAGMYFPDXBNJZSQVHLCKE"

# === Calculate the control letter for a number (DNI or NIE) ===
def calcular_letra(numero: int) -> str:
    return LETRAS_CONTROL[numero % 23]

# === Validate if a DNI (format: 8 digits + 1 letter) is valid ===
def es_dni_valido(dni: str) -> bool:
    if not re.fullmatch(r"\d{8}[A-Za-z]", dni):
        return False
    dni = dni.upper()
    numero = int(dni[:8])
    letra_correcta = calcular_letra(numero)
    return dni[-1] == letra_correcta

# === Validate if a NIE (X/Y/Z + 7 digits + 1 letter) is valid ===
def es_nie_valido(nie: str) -> bool:
    if not re.fullmatch(r"[XYZxyz]\d{7}[A-Za-z]", nie):
        return False
    nie = nie.upper()
    letra_inicial = nie[0]
    conversion = {'X': '0', 'Y': '1', 'Z': '2'}
    numero_convertido = conversion[letra_inicial] + nie[1:8]
    numero = int(numero_convertido)
    letra_correcta = calcular_letra(numero)
    return nie[-1] == letra_correcta

# === Main function to anonymize ===
def anonimizar_documentos(texto: str) -> str:
    # Search for possible documents of type DNI or NIE
    candidatos = re.findall(r"\b(?:\d{8}[A-Za-z]|[XYZxyz]\d{7}[A-Za-z])\b", texto)
    for doc in candidatos:
        if es_dni_valido(doc) or es_nie_valido(doc):
            texto = texto.replace(doc, "xxxxxxxxx")
    return texto

# === Test examples ===
def ejecutar_ejemplos():
    ejemplos = [
        "✅ Valid DNI: 12345678Z",
        "❌ Invalid DNI: 12345678A",
        "✅ Valid NIE: X1234567L",
        "✅ Valid NIE: x1234567L",
        "✅ Valid NIE: Y1234567X",
        "✅ Valid NIE: Z7654321H",
        "❌ Invalid NIE: Y1234567G",
        "❌ Invalid NIE: Z7654321R",
        "❌ NIE with invalid initial letter: A1234567Z",
        "❌ NIE with 8 digits: X12345678Z",
        "❌ My NIE is z7654321r and my DNI 87654321X",
    ]

    for i, texto in enumerate(ejemplos, 1):
        print(f"\n Example {i}")
        print("Original   :", texto)
        print("Anonymized :", anonimizar_documentos(texto))

if __name__ == "__main__":
    ejecutar_ejemplos()

