import requests
from datetime import datetime

API_URL = "https://api.citybik.es/v2/networks/bicing"

# 🚲 Estaciones
home_station_name = "C/SARDENYA, 292"
work_station_name = "AV DE LA CATEDRAL, 6"

# Limpiamos nombres para comparar sin errores
def normalizar_nombre(nombre):
    return nombre.strip().upper().replace("/", " ").replace(".", "").replace(",", "").replace("  ", " ")

# Buscar estación por nombre "limpio"
def buscar_estacion_por_nombre(estaciones, nombre_buscado):
    nombre_buscado = normalizar_nombre(nombre_buscado)
    for est in estaciones:
        if normalizar_nombre(est['name']) == nombre_buscado:
            return est
    return None

def main():
    print(f"\n🔍 Comprobando disponibilidad de Bicing a las {datetime.now().strftime('%H:%M:%S')}")
    
    # Obtener datos de Bicing
    response = requests.get(API_URL)
    if response.status_code != 200:
        print("❌ Error al obtener los datos de Bicing")
        return

    data = response.json()
    estaciones = data['network']['stations']

    # Buscar estaciones
    estacion_home = buscar_estacion_por_nombre(estaciones, home_station_name)
    estacion_work = buscar_estacion_por_nombre(estaciones, work_station_name)

    if not estacion_home:
        print(f"❌ No se encontró la estación de origen: '{home_station_name}'")
    else:
        print(f"\n🏠 Estación de origen: {estacion_home['name']}")
        print(f"   🚲 Bicis disponibles: {estacion_home['free_bikes']}")

    if not estacion_work:
        print(f"❌ No se encontró la estación de destino: '{work_station_name}'")
    else:
        print(f"\n🏢 Estación de destino: {estacion_work['name']}")
        print(f"   🅿️ Espacios libres: {estacion_work['empty_slots']}")

    # Evaluar si puedes usar Bicing
    if estacion_home and estacion_work:
        if estacion_home['free_bikes'] > 0 and estacion_work['empty_slots'] > 0:
            print("\n✅ Puedes usar Bicing para ir al trabajo ahora.")
        else:
            print("\n❌ No puedes usar Bicing ahora.")
            if estacion_home['free_bikes'] == 0:
                print("🚫 No hay bicis en la estación de origen.")
            if estacion_work['empty_slots'] == 0:
                print("🚫 No hay sitio para dejar la bici en la estación de destino.")

if __name__ == "__main__":
    main()
