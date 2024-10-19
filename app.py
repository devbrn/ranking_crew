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

# Definir tarefas que os agentes vão executar
research_task = Task(
    description="Pesquisar tendências de {topic} e gerar um relatório.",
    expected_output="Relatório de 3 parágrafos sobre as últimas tendências em {topic}.",
    agent=researcher,
)

write_task = Task(
    description="Escrever um artigo sobre {topic} baseado no relatório de tendências.",
    expected_output="Artigo de 4 parágrafos sobre {topic}, formatado em Markdown.",
    agent=writer,
)

# Criar o Crew com os agentes e as tarefas
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential
)

@app.route('/')
def home():
    return "Bem-vindo à aplicação Flask com CrewAI!"

# Rota para atribuir um novo tópico e executar as tarefas dos agentes
@app.route('/assign-task', methods=['POST'])
def assign_task():
    task_data = request.json

    if not task_data or 'topic' not in task_data:
        return jsonify({'error': 'Dados incompletos. Envie um tópico.'}), 400

    try:
        # Iniciar o Crew com o tópico definido
        result = crew.kickoff(inputs={"topic": task_data['topic']})
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/status')
def status_page():
    return render_template('index.html')

@app.route('/agents-status', methods=['GET'])
def agents_status():
    status = {
        "researcher": {"role": researcher.role, "goal": researcher.goal, "state": "Trabalhando"},
        "writer": {"role": writer.role, "goal": writer.goal, "state": "Aguardando pesquisa"}
    }
    return jsonify(status)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
