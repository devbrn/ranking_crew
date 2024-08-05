import sys
import os

# Adiciona o diretório do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from tools.custom_tool import example_tool

search_tool = SerperDevTool()

def run_crew():
    # Criando um agente pesquisador com uma ferramenta de pesquisa
    researcher = Agent(
        role='Researcher',
        goal='Conduct research on the given job description',
        backstory='You are skilled at finding the right candidates by exploring various online resources.',
        tools=[search_tool]
    )

    # Definindo a tarefa de pesquisa
    research_task = Task(
        description='Conduct research to find potential candidates for the specified job.',
        expected_output='A list of potential candidates with their profiles.',
        tools=[search_tool],
        agent=researcher,
    )

    # Criando a tripulação
    crew = Crew(
        agents=[researcher],
        tasks=[research_task],
        process=Process.sequential
    )

    # Executando a tripulação
    result = crew.kickoff()
    print(result)
