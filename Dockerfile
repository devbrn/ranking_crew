# Usar uma imagem Python leve
FROM python:3.10-slim

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar os arquivos da aplicação para o container
COPY . .

# Instalar as dependências da aplicação
RUN pip install -r requirements.txt

# Expor a porta em que o Flask vai rodar (normalmente porta 5000)
EXPOSE 5000

# Definir o comando para iniciar a aplicação Flask
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
