from crewai import Agent, Task, Crew, Process

# Criando um agente pesquisador
researcher = Agent(
    role='Pesquisador',
    goal='Pesquisar informações sobre Inteligência Artificial',
    backstory='Você é um especialista em tecnologia e pesquisa.',
    verbose=True
)

# Criando um agente escritor
writer = Agent(
    role='Escritor',
    goal='Escrever um artigo sobre o tópico pesquisado',
    backstory='Você é um escritor talentoso que transforma dados em texto.',
    verbose=True
)

# Criando as tarefas
research_task = Task(
    description='Realizar uma pesquisa detalhada sobre as tendências mais recentes em IA.',
    expected_output='Um relatório com as principais tendências em IA.',
    agent=researcher
)

write_task = Task(
    description='Escrever um artigo sobre as tendências em IA.',
    expected_output='Um artigo completo sobre IA, baseado na pesquisa realizada.',
    agent=writer
)

# Criando a tripulação (crew) e processo
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential  # Define que as tarefas serão executadas uma após a outra
)
