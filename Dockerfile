# Use a imagem oficial do Python como base
FROM python:3.10-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de requisitos para o container
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação para o container
COPY . .

# Expõe a porta que a aplicação irá rodar
EXPOSE 8000

# Comando para rodar a aplicação com Uvicorn sem reload
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
