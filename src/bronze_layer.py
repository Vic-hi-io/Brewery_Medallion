import os
import requests
import json
import logging
from datetime import datetime
from config import BRONZE_DIR


import logging

def setup_logging(log_filename="pipeline_monitoring.log"):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_filename),  # Salva logs em arquivo
            logging.StreamHandler()             # Exibe logs no console
        ]
    )

class BreweryAPIConsumer:
    def __init__(self, api_url="https://api.openbrewerydb.org/v1/breweries", bronze_dir=BRONZE_DIR):
        self.api_url = api_url
        self.bronze_dir = bronze_dir
        self.setup_logging()
        os.makedirs(bronze_dir, exist_ok=True)  # Cria o diretório da Bronze Layer se não existir

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def fetch_breweries(self, per_page=50):
        """
        Busca os dados da API e retorna uma lista de cervejarias.
        """
        breweries = []
        page = 1
        
        while True:
            try:
                self.logger.info(f"Fetching page {page}")
                params = {"per_page": per_page, "page": page}
                response = requests.get(self.api_url, params=params)
                response.raise_for_status()
                data = response.json()
                
                if not data:  # Para quando não houver mais dados
                    break
                    
                breweries.extend(data)
                page += 1
                
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Error fetching data: {e}")
                break
                
        return breweries

    def save_to_bronze(self):
        """
        Salva os dados coletados na Bronze Layer com metadados.
        """
        breweries = self.fetch_breweries()
        
        if breweries:
            # Gera um nome de arquivo com timestamp para versão
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"breweries_{timestamp}.json"
            filepath = os.path.join(self.bronze_dir, filename)
            
            # Dados com metadados
            data_with_metadata = {
                "data": breweries,
                "metadata": {
                    "source": "openbrewerydb_api",
                    "ingestion_timestamp": datetime.now().isoformat(),
                    "record_count": len(breweries)
                }
            }
            
            # Salva o JSON na Bronze Layer
            with open(filepath, 'w') as f:
                json.dump(data_with_metadata, f, indent=2)
                
            self.logger.info(f"Saved {len(breweries)} breweries to {filepath}")
            return filepath
        else:
            self.logger.warning("No data was fetched from the API")
            return None

if __name__ == "__main__":
    consumer = BreweryAPIConsumer()
    consumer.save_to_bronze()
