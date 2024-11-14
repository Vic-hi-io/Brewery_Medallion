# Pipeline de Dados de Cervejarias

## Descrição do Projeto

Este projeto implementa um pipeline de dados para coleta, transformação, e agregação de dados de cervejarias usando a API Open Brewery DB. O pipeline segue uma arquitetura de **Data Lake Medallion** com três camadas: Bronze, Silver e Gold.

## Estrutura do Projeto

- **data/bronze/**: Armazena os dados brutos coletados da API.
- **data/silver/**: Contém os dados transformados em formato Parquet, particionados por localização (estado).
- **data/gold/**: Armazena a visão agregada dos dados, com a contagem de cervejarias por tipo e estado.
- **src/**: Diretório com os scripts do pipeline:
  - `bronze_layer.py`: Script de coleta de dados para a Bronze Layer.
  - `silver_layer.py`: Script de transformação e particionamento para a Silver Layer.
  - `gold_layer.py`: Script de agregação para a Gold Layer.
  - `data_quality_checks.py`: Verificações de qualidade dos dados.

## Pré-requisitos

- Python 3.9+
- [Docker](https://docs.docker.com/get-docker/) (opcional para execução em contêiner)

## Instalação

1. Clone o repositório:

   git clone https://github.com/Vic-hi-io/Brewery_Medallion
   cd Brewery_Medallion