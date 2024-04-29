import requests
import json
import time
from datetime import datetime
import logging

# Configurações de logging
logging.basicConfig(filename='moon_api_log.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Configurações da API
url = "https://moon-phase.p.rapidapi.com/advanced"
headers = {
    "X-RapidAPI-Key": "",
    "X-RapidAPI-Host": "moon-phase.p.rapidapi.com"
}
params = {"lat": "37.7412", "lon": "-25.6756"}  # Coordenadas de São Miguel, Açores

# Pedidos à API
def fetch_data():
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Lança uma exceção para respostas 4XX ou 5XX
        data = response.json()
        logging.info("Data Extracted.")
        return data
    except requests.exceptions.HTTPError as errh:
        logging.error(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        logging.error(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        logging.error(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        logging.error(f"Error: Something Else: {err}")

# Função para guardar dados em um arquivo JSON
def save_data(data, filename):
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        logging.info(f"Data Saved to: {filename}.")
    except IOError as e:
        logging.error(f"Error : {e}")

# Executar de hora em hora até completar 120 logs
max_collections = 120  # 5 dias x 24 horas
collections_count = 0

while collections_count < max_collections:
    data = fetch_data()
    if data:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"moon_data_{timestamp}.json"
        save_data(data, filename)
        collections_count += 1
    time.sleep(3600)  # Dorme por uma hora
    
