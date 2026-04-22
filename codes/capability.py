
CRITERIOS = [
    ("largura",      "largura",      "min_pcb_larg_mm",      "max_pcb_larg_mm"),
    ("comprimento",  "comprimento",  "min_pcb_comp_mm",      "max_pcb_comp_mm"),
    ("altura",       "altura",       None,                   "max_height_limit_mm"),
    ("peso",         "peso",         None,                   "max_pcb_peso_kg"),
]


def avaliar_maquina(maquina: dict, teste: dict) -> dict:
    """
    Avalia uma única máquina contra os valores do teste.

    Parâmetros:
        maquina: dicionário com os dados da máquina (incluindo limites da espec_maquinas).
                 Ex: {"tag_maquina": "M001", "nome": "Impressora",
                      "min_pcb_larg_mm": 50, "max_pcb_larg_mm": 300, ...}
        teste:   dicionário com os valores do PCB de teste.
                 Ex: {"largura": 100, "comprimento": 150, "altura": 25, "peso": 0.5}

    Retorna:
        {
            "status": "OK" | "NOK" | "INCONCLUSIVO",
            "falhas": [...critérios que o teste violou explicitamente...],
            "campos_ausentes": [...limites da máquina que estão NULL...]
        }
    """
    falhas = []
    campos_ausentes = []

    for nome_criterio, chave_teste, chave_min, chave_max in CRITERIOS:
        valor_teste = teste.get(chave_teste)
        limite_min = maquina.get(chave_min) if chave_min else None
        limite_max = maquina.get(chave_max) if chave_max else None

        # Se o critério tem um limite mínimo esperado mas ele é None no banco,
        # marca como ausente e pula a comparação de mínimo.
        if chave_min is not None and limite_min is None:
            campos_ausentes.append(chave_min)

        # Mesma verificação para o limite máximo.
        if chave_max is not None and limite_max is None:
            campos_ausentes.append(chave_max)

        # Compara com o mínimo (se ele existe no banco).
        # Regra: valor_teste >= limite_min
        if limite_min is not None and valor_teste < limite_min:
            falhas.append(nome_criterio)
            continue  # já falhou nesse critério, não precisa testar o máximo

        # Compara com o máximo (se ele existe no banco).
        # Regra: valor_teste <= limite_max
        if limite_max is not None and valor_teste > limite_max:
            falhas.append(nome_criterio)

    # Define o status final da máquina.
    # Hierarquia: NOK domina INCONCLUSIVO, que domina OK.
    if falhas:
        status = "NOK"
    elif campos_ausentes:
        status = "INCONCLUSIVO"
    else:
        status = "OK"

    return {
        "status": status,
        "falhas": falhas,
        "campos_ausentes": campos_ausentes,
    }


def avaliar_linha(maquinas_da_linha: list, teste: dict) -> dict:
    """
    Avalia uma linha inteira (uma lista de máquinas) contra o teste.

    Parâmetros:
        maquinas_da_linha: lista de dicionários de máquina (já com espec_maquinas).
        teste: dicionário com os valores do PCB de teste.

    Retorna:
        {
            "status": "OK" | "NOK" | "INCONCLUSIVO",
            "maquinas": [
                {
                    "tag_maquina": "...",
                    "nome": "...",
                    "posicao": N,
                    "status": "OK" | "NOK" | "INCONCLUSIVO",
                    "falhas": [...],
                    "campos_ausentes": [...]
                },
                ...
            ]
        }
    """
    resultados_maquinas = []

    for maquina in maquinas_da_linha:
        resultado = avaliar_maquina(maquina, teste)
        # Monta o item de saída com os campos relevantes da máquina + o resultado.
        resultados_maquinas.append({
            "tag_maquina": maquina.get("tag_maquina"),
            "nome": maquina.get("nome"),
            "posicao": maquina.get("posicao"),
            "status": resultado["status"],
            "falhas": resultado["falhas"],
            "campos_ausentes": resultado["campos_ausentes"],
        })

    # Consolida o status da linha seguindo a hierarquia:
    # NOK > INCONCLUSIVO > OK
    algum_nok = any(m["status"] == "NOK" for m in resultados_maquinas)
    algum_inconclusivo = any(m["status"] == "INCONCLUSIVO" for m in resultados_maquinas)

    if algum_nok:
        status_linha = "NOK"
    elif algum_inconclusivo:
        status_linha = "INCONCLUSIVO"
    else:
        status_linha = "OK"

    return {
        "status": status_linha,
        "maquinas": resultados_maquinas,
    }

def calcular_linha(maquinas_da_linha: list) -> dict:
    """
    Calcula o "Bloco" da linha: o intervalo efetivo que a linha inteira
    consegue processar, considerando a máquina mais restritiva de cada critério.

    Para limites MÍNIMOS → pega o MAIOR valor entre as máquinas (o mais restritivo).
    Para limites MÁXIMOS → pega o MENOR valor entre as máquinas (o mais restritivo).
    Máquinas com campo ausente são ignoradas no cálculo daquele campo.

    Parâmetros:
        maquinas_da_linha: lista de dicionários de máquina (com spec_maquinas).

    Retorna:
        {
            "min_pcb_larg_mm": valor ou None,
            "max_pcb_larg_mm": valor ou None,
            "min_pcb_comp_mm": valor ou None,
            "max_pcb_comp_mm": valor ou None,
            "max_height_limit_mm": valor ou None,
            "max_pcb_peso_kg": valor ou None,
        }
    """
    campos_minimos = ["min_pcb_larg_mm", "min_pcb_comp_mm"]
    campos_maximos = ["max_pcb_larg_mm", "max_pcb_comp_mm",
                      "max_height_limit_mm", "max_pcb_peso_kg"]

    envelope = {}

    for campo in campos_minimos:
        valores = [m.get(campo) for m in maquinas_da_linha if m.get(campo) is not None]
        envelope[campo] = max(valores) if valores else None

    for campo in campos_maximos:
        valores = [m.get(campo) for m in maquinas_da_linha if m.get(campo) is not None]
        envelope[campo] = min(valores) if valores else None

    return envelope