# Usar uma imagem base Python
FROM python:3.9-slim

# Criar e definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos de requisitos
COPY requirements.txt .

# Instalar as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código do projeto
COPY src/ ./src/
COPY data/ ./data/

# Criar diretórios para as camadas do data lake se não existirem
RUN mkdir -p data/bronze data/silver data/gold

# Comando para executar o pipeline começando pela camada bronze
CMD ["python", "./src/bronze_layer.py"]