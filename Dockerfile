# Use uma imagem base oficial do Python 3.10
FROM python:3.10

# Defina o diretório de trabalho
WORKDIR /app

# Copie os arquivos do projeto para o contêiner
COPY . /app

# Instale as dependências do projeto, incluindo as ferramentas
RUN pip install 'crewai[tools]==0.5.0'

# Comando para iniciar a aplicação
CMD ["python", "src/ranking_crew/main.py"]
