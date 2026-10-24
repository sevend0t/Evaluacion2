import requests
import urllib.parse

# Reemplaza con tu token real de Graphhopper obtenido en el laboratorio
KEY = "TU_API_KEY_DE_GRAPHHOPPER"

def geocodificar(lugar, key):
    geo_url = f"https://graphhopper.com/api/1/geocode?q={urllib.parse.quote(lugar)}&key={key}"
    r = requests.get(geo_url)
    if r.status_code == 200:
        data = r.json()
        if data.get("hits"):
            lat = data["hits"][0]["point"]["lat"]
            lon = data["hits"][0]["point"]["lng"]
            return lat, lon
    return None, None

while True:
    print("\n=== SISTEMA DE GEOLOCALIZACIÓN Y RUTAS (GRAPHHOPPER) ===")
    origen = input("Ingrese el punto de origen (o escriba 's' / 'salir' para terminar): ")
    if origen.lower() in ["s", "salir"]:
        print("Saliendo del programa. ¡Hasta luego!")
        break
        
    destino = input("Ingrese el punto de destino (o escriba 's' / 'salir' para terminar): ")
    if destino.lower() in ["s", "salir"]:
        print("Saliendo del programa. ¡Hasta luego!")
        break

    print("\nBuscando coordenadas y calculando la ruta óptima...")
    
    # 1. Obtener coordenadas de origen y destino mediante Geocodificación
    lat_org, lon_org = geocodificar(origen, KEY)
    lat_dest, lon_dest = geocodificar(destino, KEY)
    
    if not lat_org or not lat_dest:
        print("Error: No se pudieron encontrar las coordenadas para los lugares ingresados. Verifique los nombres e intente nuevamente.")
        continue
        
    # 2. Consultar la API de Rutas de Graphhopper (con locale=es para la narrativa en español)
    route_url = f"https://graphhopper.com/api/1/route?point={lat_org},{lon_org}&point={lat_dest},{lon_dest}&vehicle=car&locale=es&key={KEY}"
    r_route = requests.get(route_url)
    
    if r_route.status_code == 200:
        route_data = r_route.json()
        if "paths" in route_data and len(route_data["paths"]) > 0:
            path = route_data["paths"][0]
            
            # Conversión de metros a kilómetros y milisegundos a minutos
            distancia_km = path["distance"] / 1000.0
            tiempo_min = path["time"] / 60000.0
            
            print(f"\n--- INFORMACIÓN DEL VIAJE ---")
            print(f"Distancia total: {distancia_km:.2f} km")
            print(f"Tiempo estimado: {tiempo_min:.2f} minutos")
            
            print("\n--- Instrucciones paso a paso (Narrativa del viaje) ---")
            instructions = path.get("instructions", [])
            for idx, inst in enumerate(instructions, 1):
                texto = inst.get("text", "")
                dist_inst = inst.get("distance", 0) / 1000.0
                print(f"{idx}. {texto} ({dist_inst:.2f} km)")
            print("--------------------------------------------------\n")
        else:
            print("No se encontró una ruta disponible entre los puntos indicados.")
    else:
        print(f"Error al conectar con la API de Graphhopper: Código {r_route.status_code}")