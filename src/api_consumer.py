# src/api_consumer.py
import requests
import json
import logging
import os
from datetime import datetime
from config import BRONZE_DIR

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
    def __init__(self):
        self.api_url = "https://api.openbrewerydb.org/breweries"
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def fetch_breweries(self, per_page=50):
        breweries = []
        page = 1
        
        while True:
            try:
                self.logger.info(f"Fetching page {page}")
                params = {"per_page": per_page, "page": page}
                response = requests.get(self.api_url, params=params)
                response.raise_for_status()
                data = response.json()
                
                if not data:  # No more results
                    break
                    
                breweries.extend(data)
                page += 1
                
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Error fetching data: {e}")
                break
                
        return breweries

    def save_to_bronze(self):
        breweries = self.fetch_breweries()
        
        if breweries:
            # Create filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"breweries_{timestamp}.json"
            filepath = os.path.join(BRONZE_DIR, filename)
            
            # Save data with metadata
            data_with_metadata = {
                "data": breweries,
                "metadata": {
                    "source": "openbrewerydb_api",
                    "ingestion_timestamp": datetime.now().isoformat(),
                    "record_count": len(breweries)
                }
            }
            
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