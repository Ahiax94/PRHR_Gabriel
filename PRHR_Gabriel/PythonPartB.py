import re

# === Letras oficiales de control ===
LETRAS_CONTROL = "TRWAGMYFPDXBNJZSQVHLCKE"

# === Calcula la letra de control para un número (DNI o NIE) ===
def calcular_letra(numero: int) -> str:
    return LETRAS_CONTROL[numero % 23]

# === Valida si un DNI (formato 8 números + 1 letra) es válido ===
def es_dni_valido(dni: str) -> bool:
    if not re.fullmatch(r"\d{8}[A-Za-z]", dni):
        return False
    dni = dni.upper()
    numero = int(dni[:8])
    letra_correcta = calcular_letra(numero)
    return dni[-1] == letra_correcta

# === Valida si un NIE (X/Y/Z + 7 números + 1 letra) es válido ===
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

# === Función principal para anonimizar ===
def anonimizar_documentos(texto: str) -> str:
    # Busca posibles documentos tipo DNI o NIE
    candidatos = re.findall(r"\b(?:\d{8}[A-Za-z]|[XYZxyz]\d{7}[A-Za-z])\b", texto)
    for doc in candidatos:
        if es_dni_valido(doc) or es_nie_valido(doc):
            texto = texto.replace(doc, "xxxxxxxxx")
    return texto

# === Ejemplos de prueba ===
def ejecutar_ejemplos():
    ejemplos = [
        "✅ DNI válido: 12345678Z",
        "❌ DNI inválido: 12345678A",
        "✅ NIE válido: X1234567L",
        "✅ NIE válido: x1234567L",
        "✅ NIE válido: Y1234567X",
        "✅ NIE válido: Z7654321H",
        "❌ NIE inválido: Y1234567G",
        "❌ NIE inválido: Z7654321R",
        "❌ NIE con letra inicial inválida: A1234567Z",
        "❌ NIE con 8 dígitos: X12345678Z",
        "❌Mi NIE es z7654321r y mi DNI 87654321X",
    ]

    for i, texto in enumerate(ejemplos, 1):
        print(f"\n Ejemplo {i}")
        print("Original   :", texto)
        print("Anonimizado:", anonimizar_documentos(texto))

if __name__ == "__main__":
    ejecutar_ejemplos()
