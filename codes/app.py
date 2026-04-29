from flask import Flask, render_template, jsonify, request
import CRUD
from capability import avaliar_linha, calcular_linha

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

@app.route('/api/capabilidade/testar', methods=['POST'])
def testar_capabilidade():
    """
    Recebe os dados de um PCB de teste e retorna o resultado da avaliação
    de capabilidade por linha e por máquina.

    Body esperado:
        {
            "largura": 150,         # obrigatório (mm)
            "comprimento": 200,     # obrigatório (mm)
            "altura": 25,           # obrigatório (mm)
            "peso": 0.5,            # obrigatório (kg)
            "linha": 2              # opcional — se omitido, avalia todas as linhas
        }

    Retorna:
        {
            "sucesso": true,
            "teste": { ...dados recebidos... },
            "linhas": [
                {
                    "linha": 1,
                    "status": "OK" | "NOK",
                    "maquinas": [
                        {
                            "tag_maquina": "...",
                            "nome": "...",
                            "posicao": 1,
                            "status": "OK" | "NOK" | "INCONCLUSIVO",
                            "falhas": [...],
                            "campos_ausentes": [...]
                        },
                        ...
                    ]
                },
                ...
            ]
        }
    """
    # 1. Pega o JSON do corpo da requisição
    dados = request.get_json()

    if not dados:
        return jsonify({
            "sucesso": False,
            "mensagem": "Nenhum dado recebido."
        }), 400

    # 2. Valida que os 4 campos do PCB estão presentes e são numéricos
    campos_obrigatorios = ["largura", "comprimento", "altura", "peso"]
    teste = {}

    for campo in campos_obrigatorios:
        valor = dados.get(campo)
        if valor is None or valor == "":
            return jsonify({
                "sucesso": False,
                "mensagem": f"Campo obrigatório ausente: {campo}."
            }), 400
        try:
            teste[campo] = float(valor)
        except (TypeError, ValueError):
            return jsonify({
                "sucesso": False,
                "mensagem": f"Campo '{campo}' deve ser um número."
            }), 400

    # 3. Pega o filtro opcional de linha
    linha_filtro = dados.get("linha")
    if linha_filtro is not None and linha_filtro != "":
        # Normaliza pra string (linha pode ser nome ou número)
        linha_filtro = str(linha_filtro).strip()
    else:
        linha_filtro = None  # normaliza string vazia para None

    # 4. Busca todas as máquinas agrupadas por linha
    todas_as_linhas = CRUD.listar_maquinas_agrupadas_por_linha()

    # 5. Se o usuário pediu uma linha específica, filtra
    if linha_filtro is not None:
        if linha_filtro not in todas_as_linhas:
            return jsonify({
                "sucesso": False,
                "mensagem": f"Linha {linha_filtro} não encontrada ou sem máquinas."
            }), 404
        linhas_para_avaliar = {linha_filtro: todas_as_linhas[linha_filtro]}
    else:
        linhas_para_avaliar = todas_as_linhas

    # 6. Avalia cada linha e monta a resposta
    resultado_linhas = []
    for numero_linha in sorted(linhas_para_avaliar.keys()):
        maquinas_da_linha = linhas_para_avaliar[numero_linha]
        resultado_linha = avaliar_linha(maquinas_da_linha, teste)
        envelope = calcular_linha(maquinas_da_linha)

        resultado_linhas.append({
            "linha": numero_linha,
            "status": resultado_linha["status"],
            "envelope": envelope,
            "maquinas": resultado_linha["maquinas"],
        })

    # 7. Retorna a resposta completa
    return jsonify({
        "sucesso": True,
        "teste": teste,
        "linhas": resultado_linhas,
})


@app.route('/capability')
def tela_capabilidade():
    return render_template('capability.html')

@app.route('/lineview')
def tela_lineview():
    return render_template('lineview.html')

if __name__ == '__main__':
    app.run(debug=True)

    