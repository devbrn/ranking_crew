from flask import Flask, jsonify, render_template, request
from crew import crew  # Importando o CrewAI e a tripulação

app = Flask(__name__)

@app.route('/')
def home():
    return "Bem-vindo à aplicação Flask com CrewAI!"

# Rota para iniciar o crew e delegar tarefas dinâmicas
@app.route('/assign-task', methods=['POST'])
def assign_task():
    task_data = request.json  # Esperando dados em formato JSON

    # Exemplo: atribuindo ao pesquisador
    task = Task(
        description=task_data.get('description'),
        expected_output=task_data.get('expected_output'),
        agent=crew.agents[0]  # Assignando ao pesquisador (por exemplo)
    )
    
    # Executa a tarefa
    result = task.run()
    
    # Retorna o resultado da tarefa
    return jsonify({'result': result})

@app.route('/status')
def status_page():
    return render_template('index.html')

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
    else:
        status = {'error': 'Agentes não encontrados.'}
    
    return jsonify(status)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
