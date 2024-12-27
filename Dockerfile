# Usa a imagem oficial do Python como base
FROM python:3.12-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo de requisitos do Python para o contêiner
COPY requirements.txt .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código para o contêiner
COPY . .

# Expõe a porta que a aplicação usará (5000 no Flask)
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["python", "app.py"]
