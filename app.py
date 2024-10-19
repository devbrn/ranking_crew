from flask import Flask, jsonify, render_template
from crew import crew  # Importando a configuração do CrewAI

app = Flask(__name__)

@app.route('/')
def home():
    return "Bem-vindo à aplicação Flask com CrewAI!"

@app.route('/start-crew', methods=['GET'])
def start_crew():
    result = crew.kickoff()
    return jsonify(result)

@app.route('/status')
def status_page():
    return render_template('index.html')

@app.route('/agents-status', methods=['GET'])
def agents_status():
    # Verificar se os agentes existem antes de acessar
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
