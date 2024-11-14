# src/transform_to_silver.py

import os
import json
import pandas as pd
from datetime import datetime
from config import SILVER_DIR, BRONZE_DIR

class BreweryDataTransformer:
    def __init__(self, bronze_dir=BRONZE_DIR, silver_dir=SILVER_DIR):
        self.bronze_dir = bronze_dir
        self.silver_dir = silver_dir
        os.makedirs(silver_dir, exist_ok=True)  # Cria o diretório Silver Layer se não existir

    def load_bronze_data(self):
        """
        Carrega os dados brutos da Bronze Layer.
        """
        all_data = []
        for filename in os.listdir(self.bronze_dir):
            if filename.endswith(".json"):
                with open(os.path.join(self.bronze_dir, filename), 'r') as f:
                    data = json.load(f)
                    all_data.extend(data["data"])  # Extrai apenas a lista de dados

        return pd.DataFrame(all_data)

    def transform_and_partition_data(self, df):
        """
        Transforma os dados e particiona por localização (estado).
        """
        # Converter colunas para garantir compatibilidade
        df["state"] = df["state"].fillna("Unknown")  # Lida com valores nulos na coluna de localização
        df["brewery_type"] = df["brewery_type"].fillna("Unknown")  # Lida com valores nulos em tipo de cervejaria
        
        # Filtrar colunas relevantes para análise
        columns_of_interest = ["id", "name", "brewery_type", "street", "city", "state", "country", "longitude", "latitude"]
        df = df[columns_of_interest]

        # Adicionar timestamp de processamento
        df["processing_timestamp"] = datetime.now().isoformat()

        # Particionar por estado e salvar em formato Parquet na Silver Layer
        for state, partition_df in df.groupby("state"):
            state_dir = os.path.join(self.silver_dir, f"state={state}")
            os.makedirs(state_dir, exist_ok=True)
            
            # Salva em formato Parquet
            partition_df.to_parquet(os.path.join(state_dir, f"breweries_{state}.parquet"), index=False)

    def process_data(self):
        """
        Processa os dados da Bronze Layer e salva na Silver Layer em formato Parquet, particionado por localização.
        """
        # Carregar dados da Bronze Layer
        df = self.load_bronze_data()
        
        # Transformar e particionar dados
        self.transform_and_partition_data(df)
        print("Dados processados e salvos na Silver Layer com sucesso.")

if __name__ == "__main__":
    transformer = BreweryDataTransformer()
    transformer.process_data()