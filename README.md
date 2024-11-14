# Pipeline de Dados de Cervejarias (PT-BR)

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


# Orquestração com AWS Step Functions

O pipeline é orquestrado pelo AWS Step Functions, que coordena a execução das camadas Bronze, Silver e Gold. Cada camada é configurada como uma função AWS Lambda, e o Step Functions gerencia a sequência de execução e o monitoramento do processo.

# Fluxo de Trabalho no AWS Step Functions

Bronze Layer: Coleta os dados da API e os armazena na camada Bronze em formato bruto.
Silver Layer: Processa e transforma os dados da Bronze Layer em Parquet, particionando-os por localização.
Gold Layer: Gera uma visão agregada dos dados transformados para análise.

# Instruções para Configuração no AWS Step Functions

Para configurar o pipeline no AWS Step Functions:

Crie funções AWS Lambda para cada camada (BronzeLayerFunction, SilverLayerFunction, GoldLayerFunction) e faça upload do respectivo código Python para cada função.
No AWS Step Functions, crie uma nova máquina de estados que orquestre as três funções Lambda em sequência. Defina o fluxo de trabalho para executar a BronzeLayerFunction, seguida pela SilverLayerFunction e, por fim, a GoldLayerFunction.
Configure políticas de retry e captura de erros para garantir a robustez do pipeline.
O Step Functions permite monitorar o status de cada etapa e gerenciar reexecuções em caso de falhas, garantindo que o pipeline seja executado de maneira confiável.


## Pré-requisitos

- Conta AWS com permissões para AWS Lambda e Step Functions
- Python 3.9+
- [Docker](https://docs.docker.com/get-docker/) (opcional para execução em contêiner)

## Estrutura do Docker
O projeto inclui:

`Dockerfile`: Configuração para criar a imagem Docker
`requirements.txt`: Lista de dependências Python necessárias

## Instalação

1. Clone o repositório:

   git clone https://github.com/Vic-hi-io/Brewery_Medallion
   cd Brewery_Medallion

################################################################################################################################################

# Brewery Data Pipeline (EN)

## Project Description

This project implements a data pipeline for collecting, transforming, and aggregating brewery data using the Open Brewery DB API. The pipeline follows a **Data Lake Medallion** architecture with three layers: Bronze, Silver, and Gold.

## Project Structure

- **data/bronze/**: Stores the raw data collected from the API.
- **data/silver/**: Contains the transformed data in Parquet format, partitioned by location (state).
- **data/gold/**: Stores the aggregated view of the data, with the count of breweries by type and state.
- **src/**: Directory with the pipeline scripts:
- `bronze_layer.py`: Data collection script for the Bronze Layer.
- `silver_layer.py`: Transformation and partitioning script for the Silver Layer.
- `gold_layer.py`: Aggregation script for the Gold Layer.
- `data_quality_checks.py`: Data quality checks.

# Orchestration with AWS Step Functions

The pipeline is orchestrated by AWS Step Functions, which coordinates the execution of the Bronze, Silver, and Gold layers. Each layer is configured as an AWS Lambda function, and Step Functions manages the execution sequence and monitoring of the process.

# Workflow in AWS Step Functions

Bronze Layer: Collects data from the API and stores it in the Bronze layer in raw format.
Silver Layer: Processes and transforms the data from the Bronze Layer into Parquet, partitioning it by location.
Gold Layer: Generates an aggregated view of the transformed data for analysis.

# AWS Step Functions Setup Instructions

To set up your pipeline in AWS Step Functions:

Create AWS Lambda functions for each layer (BronzeLayerFunction, SilverLayerFunction, GoldLayerFunction) and upload the corresponding Python code for each function.
In AWS Step Functions, create a new state machine that orchestrates the three Lambda functions in sequence. Define the workflow to execute the BronzeLayerFunction, followed by the SilverLayerFunction, and finally the GoldLayerFunction.
Configure retry and error-catching policies to ensure the robustness of your pipeline.
Step Functions allows you to monitor the status of each step and manage reruns in case of failures, ensuring that your pipeline runs reliably.

## Prerequisites

- AWS account with permissions for AWS Lambda and Step Functions
- Python 3.9+
- [Docker](https://docs.docker.com/get-docker/) (optional for running in a container)

## Docker framework
The project includes:

`Dockerfile`: Configuration for building the Docker image
`requirements.txt`: List of required Python dependencies

## Installation

1. Clone the repository:

git clone https://github.com/Vic-hi-io/Brewery_Medallion
cd Brewery_Medallion