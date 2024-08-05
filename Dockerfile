# Use uma imagem base oficial do Python
FROM python:3.9

# Defina o diretório de trabalho
WORKDIR /app

# Copie os arquivos do projeto para o contêiner
COPY . /app

# Criar o arquivo requirements.txt
RUN echo "crewai\ncrewai_tools" > requirements.txt

# Instale as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Comando para iniciar a aplicação
CMD ["python", "src/<ranking_crew>/main.py"]
