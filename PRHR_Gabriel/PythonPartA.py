import requests
from datetime import datetime
# I wasn’t sure whether I should look at the hardcoded time or use the current time.
# I opted for the latter, as I think it makes the script more useful you could run it multiple times before 8:50 AM to check if there are any bikes or available spaces.
API_URL = "https://api.citybik.es/v2/networks/bicing"

# 🚲 Stations
home_station_name = "C/SARDENYA, 292"
work_station_name = "AV DE LA CATEDRAL, 6"

# Clean names to compare without errors
def normalizar_nombre(nombre):
    return nombre.strip().upper().replace("/", " ").replace(".", "").replace(",", "").replace("  ", " ")

# Search station by "clean" name
def buscar_estacion_por_nombre(estaciones, nombre_buscado):
    nombre_buscado = normalizar_nombre(nombre_buscado)
    for est in estaciones:
        if normalizar_nombre(est['name']) == nombre_buscado:
            return est
    return None

def main():
    print(f"\n🔍 Checking Bicing availability at {datetime.now().strftime('%H:%M:%S')}")
    
    # Get Bicing data
    response = requests.get(API_URL)
    if response.status_code != 200:
        print("❌ Error getting Bicing data")
        return

    data = response.json()
    estaciones = data['network']['stations']

    # Search stations
    estacion_home = buscar_estacion_por_nombre(estaciones, home_station_name)
    estacion_work = buscar_estacion_por_nombre(estaciones, work_station_name)

    if not estacion_home:
        print(f"❌ Origin station not found: '{home_station_name}'")
    else:
        print(f"\n🏠 Origin station: {estacion_home['name']}")
        print(f"   🚲 Bikes available: {estacion_home['free_bikes']}")

    if not estacion_work:
        print(f"❌ Destination station not found: '{work_station_name}'")
    else:
        print(f"\n🏢 Destination station: {estacion_work['name']}")
        print(f"   🅿️ Free slots: {estacion_work['empty_slots']}")

    # Evaluate if you can use Bicing
    if estacion_home and estacion_work:
        if estacion_home['free_bikes'] > 0 and estacion_work['empty_slots'] > 0:
            print("\n✅ You can use Bicing to go to work now.")
        else:
            print("\n❌ You can't use Bicing now.")
            if estacion_home['free_bikes'] == 0:
                print("🚫 No bikes available at the origin station.")
            if estacion_work['empty_slots'] == 0:
                print("🚫 No space to leave the bike at the destination station.")

if __name__ == "__main__":
    main()
