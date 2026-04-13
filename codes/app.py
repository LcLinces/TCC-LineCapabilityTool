from flask import Flask, render_template, jsonify, request
import CRUD

app = Flask(__name__)

# Rota principal — entrega só o HTML da página
@app.route('/')
def index():
    return render_template('index.html')

# API — retorna TODAS as máquinas em JSON (para o JavaScript popular o sidebar)
@app.route('/api/maquinas')
def api_maquinas():
    maquinas = CRUD.buscar_todas_maquinas_resumo()
    return jsonify(maquinas)

# API — retorna UMA máquina completa em JSON (para o JavaScript popular o painel direito)
@app.route('/api/maquina/<tag>')
def api_maquina(tag):
    maquina = CRUD.buscar_maquina_completa(tag)
    if not maquina:
        return jsonify({'erro': 'Não encontrada'}), 404
    return jsonify(maquina)

# Rota para criação de nova máquina
@app.route('/api/maquina/nova', methods=['POST'])
def api_nova_maquina():
    dados = request.get_json()
    sucesso, mensagem =CRUD.create(dados)
    return jsonify({'sucesso': sucesso, 'mensagem': mensagem})

if __name__ == '__main__':
    app.run(debug=True)