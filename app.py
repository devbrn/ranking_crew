from flask import Flask, jsonify, render_template, request
from crew import crew  # Importando o CrewAI e a tripulação
from crewai import Task
import logging

# Configurando logging para mostrar no console
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Rota principal
@app.route('/')
def home():
    return "Bem-vindo à aplicação Flask com CrewAI!"

# Rota para iniciar o CrewAI e delegar tarefas dinâmicas
@app.route('/assign-task', methods=['POST'])  # Aceitar apenas requisições POST
def assign_task():
    # Receber dados da tarefa enviados via POST em formato JSON
    task_data = request.json

    # Garantir que a descrição e o resultado esperado foram enviados
    if not task_data or 'description' not in task_data or 'expected_output' not in task_data:
        logger.error("Dados incompletos. Envie a descrição e o resultado esperado.")
        return jsonify({'error': 'Dados incompletos. Envie a descrição e o resultado esperado da tarefa.'}), 400

    try:
        logger.info("Recebendo tarefa: %s", task_data['description'])
        
        # Criar uma nova tarefa para o agente Pesquisador
        task = Task(
            description=task_data['description'],
            expected_output=task_data['expected_output'],
            agent=crew.agents[0]  # Atribuir ao Pesquisador (primeiro agente)
        )

        # Adicionar a nova tarefa ao Crew
        crew.tasks.append(task)

        # Executar todas as tarefas (inclusive a nova) usando o kickoff
        result = crew.kickoff()

        # Logar o resultado e retornar a resposta
        logger.info("Tarefa concluída. Resultado: %s", result)
        return jsonify({'result': result})
    except Exception as e:
        logger.error("Erro ao executar a tarefa: %s", str(e))
        return jsonify({'error': str(e)}), 500

# Rota para renderizar a página de status
@app.route('/status')
def status_page():
    return render_template('index.html')

# Rota para retornar o status atual dos agentes em formato JSON
@app.route('/agents-status', methods=['GET'])
def agents_status():
    if len(crew.agents) >= 2:
        status = {
            'researcher': {
                'role': crew.agents[0].role,
                'goal': crew.agents[0].goal,
                'state': 'Trabalhando'
            },
            'writer': {
                'role': crew.agents[1].role,
                'goal': crew.agents[1].goal,
                'state': 'Aguardando pesquisa'
            }
        }
        logger.info("Status dos agentes: %s", status)
    else:
        status = {'error': 'Agentes não encontrados.'}
        logger.error("Nenhum agente encontrado.")
    
    return jsonify(status)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
