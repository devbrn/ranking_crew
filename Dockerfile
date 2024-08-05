# Use uma imagem base oficial do Python 3.10
FROM python:3.10

# Defina o diretório de trabalho
WORKDIR /app

# Copie os arquivos do projeto para o contêiner
COPY . /app

# Criar o arquivo requirements.txt com versões específicas
RUN echo "crewai==0.5.0\ncrewai_tools==0.2.0\nlangchain==0.1.0" > requirements.txt

# Instale as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Comando para iniciar a aplicação
CMD ["python", "src/ranking_crew/main.py"]
