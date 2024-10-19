import os
from flask import Flask, jsonify, render_template, request
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool  # Exemplo de ferramenta

app = Flask(__name__)

# Configurar as chaves de API necessárias
os.environ["SERPER_API_KEY"] = "sua_api_key"
os.environ["OPENAI_API_KEY"] = "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"

# Definir a ferramenta para pesquisa (exemplo)
search_tool = SerperDevTool()

# Criar agentes com suas respectivas funções e metas
researcher = Agent(
    role="Pesquisador",
    goal="Pesquisar tendências sobre {topic}",
    tools=[search_tool],
    verbose=True,
    memory=True,
    backstory=(
        "Você é um pesquisador especialista em novas tecnologias e está sempre atento"
        "às últimas tendências no campo de {topic}."
    )
)

writer = Agent(
    role="Escritor",
    goal="Escrever um artigo sobre {topic}",
    tools=[search_tool],
    verbose=True,
    memory=True,
    backstory=(
        "Você é um escritor experiente, especializado em simplificar tópicos complexos"
        "e tornar as informações acessíveis para todos."
    )
)

# Definir o endpoint para atribuir tarefas
@app.route('/assign-task', methods=['POST'])
def assign_task():
    task_data = request.json

    if not task_data or 'description' not in task_data or 'agent' not in task_data:
        return jsonify({'error': 'Dados incompletos. Envie uma descrição e o agente.'}), 400

    agent_name = task_data['agent']
    if agent_name == 'researcher':
        agent = researcher
    elif agent_name == 'writer':
        agent = writer
    else:
        return jsonify({'error': 'Agente desconhecido.'}), 400

    try:
        # Criar a tarefa com o agente selecionado
        task = Task(
            description=task_data['description'],
            expected_output=task_data['expected_output'],
            agent=agent
        )
        crew = Crew(agents=[agent], tasks=[task], process=Process.sequential)
        result = crew.kickoff(inputs={"topic": task_data['description']})
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
