# src/aggregate_to_gold.py

import os
import pandas as pd
from config import SILVER_DIR, GOLD_DIR

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


class BreweryDataAggregator:
    def __init__(self, silver_dir=SILVER_DIR, gold_dir=GOLD_DIR):
        self.silver_dir = silver_dir
        self.gold_dir = gold_dir
        os.makedirs(gold_dir, exist_ok=True)  # Cria o diretório Gold Layer se não existir

    def load_silver_data(self):
        """
        Carrega todos os arquivos Parquet da Silver Layer em um único DataFrame.
        """
        all_data = []
        
        # Percorre cada subdiretório da Silver Layer para carregar os arquivos Parquet
        for root, dirs, files in os.walk(self.silver_dir):
            for file in files:
                if file.endswith(".parquet"):
                    file_path = os.path.join(root, file)
                    df = pd.read_parquet(file_path)
                    all_data.append(df)

        # Concatena todos os DataFrames em um único DataFrame
        return pd.concat(all_data, ignore_index=True)

    def aggregate_data(self, df):
        """
        Agrega os dados para contar o número de cervejarias por tipo e estado.
        """
        # Cria a agregação para contar o número de cervejarias por tipo e estado
        aggregated_df = df.groupby(["state", "brewery_type"]).size().reset_index(name="brewery_count")

        return aggregated_df

    def save_aggregated_data(self, aggregated_df):
        """
        Salva os dados agregados na Gold Layer em formato Parquet.
        """
        filepath = os.path.join(self.gold_dir, "brewery_aggregated_by_type_and_state.parquet")
        
        # Salva o DataFrame agregado como Parquet
        aggregated_df.to_parquet(filepath, index=False)
        print(f"Dados agregados salvos em: {filepath}")

    def process_data(self):
        """
        Executa o pipeline completo da Gold Layer: carrega, agrega e salva os dados.
        """
        # Carregar dados da Silver Layer
        df = self.load_silver_data()
        
        # Agregar dados
        aggregated_df = self.aggregate_data(df)
        
        # Salvar dados agregados na Gold Layer
        self.save_aggregated_data(aggregated_df)
        print("Pipeline da Gold Layer completo.")

if __name__ == "__main__":
    aggregator = BreweryDataAggregator()
    aggregator.process_data()
