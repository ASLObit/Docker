import requests
import sys

def check_simit(plate):
    """
    Consulta la API de datos abiertos para verificar multas de SIMIT por placa.
    Retorna el número de multas encontradas.
    """
    # Identificador del conjunto de datos para "Historial de Multas reportados en el SIMIT".
    dataset_id = "72nf-y4v3"
    
    # Construye la URL de la API SODA.
    api_url = f"https://www.datos.gov.co/resource/{dataset_id}.json"
    
    # Construye la consulta SoQL para filtrar por placa.
    # Se debe sanitizar la entrada si se utiliza en un entorno de producción para prevenir inyecciones.
    query_params = {
        "$where": f"upper(placa) = '{plate.upper()}'"
    }
    
    try:
        response = requests.get(api_url, params=query_params)
        response.raise_for_status()  # Lanza un error si la petición falla.
        
        data = response.json()
        num_fines = len(data)
        
        print(num_fines)
        return num_fines
        
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}", file=sys.stderr)
        return -1
    except Exception as e:
        print(f"Error inesperado: {e}", file=sys.stderr)
        return -1

if __name__ == "__main__":
    # La placa del vehículo debe ser pasada como un argumento.
    if len(sys.argv) < 2:
        print("Uso: python simit_checker.py <placa>", file=sys.stderr)
        sys.exit(1)
        
    vehicle_plate = sys.argv[27]
    check_simit(vehicle_plate)