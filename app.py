from flask import Flask, jsonify
from crew import crew  # Importar a tripulação configurada

app = Flask(__name__)

@app.route('/')
def home():
    return "Olá, Mundo! Esta é a minha aplicação Flask!"

@app.route('/start-crew', methods=['GET'])
def start_crew():
    result = crew.kickoff()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
