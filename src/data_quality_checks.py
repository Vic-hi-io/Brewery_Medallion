# src/data_quality_checks.py

import pandas as pd
import os
import logging
import smtplib
from email.message import EmailMessage
from config import GOLD_DIR
 

def setup_logging(log_filename="pipeline_monitoring.log"):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_filename),  # Salva logs em arquivo
            logging.StreamHandler()             # Exibe logs no console
        ]
    )

class DataQualityChecker:
    def __init__(self, gold_dir=GOLD_DIR):
        self.gold_dir = gold_dir
        self.filepath = os.path.join(gold_dir, "brewery_aggregated_by_type_and_state.parquet")
    
    def check_for_nulls(self):
        """
        Verifica se há valores nulos nas colunas críticas da Gold Layer.
        """
        if not os.path.exists(self.filepath):
            logging.error("Arquivo de dados agregado não encontrado.")
            return False

        df = pd.read_parquet(self.filepath)
        
        # Verificar valores nulos nas colunas críticas
        nulls = df.isnull().sum()
        if nulls.any():
            logging.warning(f"Valores nulos encontrados: \n{nulls[nulls > 0]}")
            return False
        else:
            logging.info("Nenhum valor nulo encontrado nas colunas críticas.")
            return True

    def check_record_count(self):
        """
        Verifica se a contagem de registros é consistente.
        """
        df = pd.read_parquet(self.filepath)
        record_count = len(df)
        
        if record_count == 0:
            logging.warning("A tabela de dados agregados está vazia.")
            return False
        else:
            logging.info(f"Contagem de registros: {record_count}")
            return True

    def run_all_checks(self):
        """
        Executa todas as verificações de qualidade de dados.
        """
        checks = [
            self.check_for_nulls(),
            self.check_record_count()
        ]
        if all(checks):
            logging.info("Todas as verificações de qualidade de dados foram aprovadas.")
        else:
            logging.warning("Algumas verificações de qualidade de dados falharam.")

if __name__ == "__main__":
    setup_logging()  # Chamar função de configuração de log
    checker = DataQualityChecker()
    checker.run_all_checks()
