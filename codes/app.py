from flask import Flask, render_template, jsonify, request
import CRUD

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/maquinas')
def api_maquinas():
    maquinas = CRUD.buscar_todas_maquinas_resumo()
    return jsonify(maquinas)

# ← Rota fixa ANTES da rota dinâmica <tag>
@app.route('/api/maquina/nova', methods=['POST'])
def api_nova_maquina():
    dados = request.get_json()
    sucesso, mensagem = CRUD.create(dados)
    return jsonify({'sucesso': sucesso, 'mensagem': mensagem})

# ← Rotas dinâmicas DEPOIS
@app.route('/api/maquina/<tag>')
def api_maquina(tag):
    maquina = CRUD.buscar_maquina_completa(tag)
    if not maquina:
        return jsonify({'erro': 'Não encontrada'}), 404
    return jsonify(maquina)

@app.route('/api/maquina/<tag>/editar', methods=['POST'])
def api_editar_maquina(tag):
    dados = request.get_json()
    sucesso, mensagem = CRUD.update(tag, dados)
    return jsonify({'sucesso': sucesso, 'mensagem': mensagem})

@app.route('/api/maquina/<tag>/deletar', methods=['POST'])
def api_deletar_maquina(tag):
    sucesso, mensagem = CRUD.delete(tag)
    return jsonify({'sucesso': sucesso, 'mensagem': mensagem})

if __name__ == '__main__':
    app.run(debug=True)