from CRUD import create

# Função auxiliar de engenharia para tratar os inputs do terminal
def obter_dado(mensagem, tipo=str, obrigatorio=False):
    while True:
        valor = input(mensagem).strip()
        
        if not valor:  # Se o usuário apenas apertou Enter (vazio)
            if obrigatorio:
                print("Campo obrigatório. Por favor, preencha.")
                continue
            return None # Retorna None (Nulo no banco de dados)
            
        try:
            return tipo(valor) # Tenta converter para o tipo correto (float, int, etc)
        except ValueError:
            print(f"Valor inválido. Esperado um formato numérico.")

def main():
    print("="*50)
    print(" SISTEMA DE CADASTRO DE MÁQUINAS (MODO TERMINAL)")
    print("="*50)
    print("Dica: Aperte ENTER para pular os campos não obrigatórios.\n")

    dados = {}

    print("--- 1. DADOS GERAIS ---")
    dados['tag_maquina'] = obter_dado("Tag da Máquina [Obrigatório, Ex: MAQ - 001]: ", str, True)
    dados['serial_No'] = obter_dado("Número de Série: ")
    dados['nome_maquina'] = obter_dado("Nome / Modelo [Obrigatório]: ", str, True)
    dados['tipo'] = obter_dado("Tipo (ex: Pick & Place) [Obrigatório]: ", str, True)
    dados['tensao_v'] = obter_dado("Tensão Elétrica (V): ", float)
    dados['frequencia_hz'] = obter_dado("Frequência (Hz): ", float)
    dados['potencia'] = obter_dado("Potência: ", float)
    dados['unidade_potencia'] = obter_dado("Unidade de Potência (ex: kW): ")
    dados['pressao'] = obter_dado("Pressão Pneumática: ", float)
    dados['unidade_pressao'] = obter_dado("Unidade de Pressão (ex: bar): ")
    dados['comentario'] = obter_dado("Comentários/Observações: ")

    print("\n--- 2. ESPECIFICAÇÕES OPERACIONAIS (PCB) ---")
    dados['max_pcb_peso_kg'] = obter_dado("Peso Máx. da Placa (kg): ", float)
    dados['min_pcb_comp_mm'] = obter_dado("Comp. Mín. da Placa (mm): ", float)
    dados['min_pcb_larg_mm'] = obter_dado("Largura Mín. da Placa (mm): ", float)
    dados['max_pcb_comp_mm'] = obter_dado("Comp. Máx. da Placa (mm): ", float)
    dados['max_pcb_larg_mm'] = obter_dado("Largura Máx. da Placa (mm): ", float)
    dados['max_height_limit_mm'] = obter_dado("Altura Máx. Componentes (mm): ", float)

    print("\n--- 3. DIMENSÕES FÍSICAS DA MÁQUINA ---")
    dados['peso_maquina'] = obter_dado("Peso da Máquina (kg): ", float)
    dados['comp_maquina'] = obter_dado("Comprimento da Máquina (mm): ", float)
    dados['larg_maquina'] = obter_dado("Largura da Máquina (mm): ", float)
    dados['alt_maquina'] = obter_dado("Altura da Máquina (mm): ", float)

    print("\n--- 4. LAYOUT / POSICIONAMENTO ---")
    dados['linha'] = obter_dado("Linha de Produção (ex: SMT-1): ")
    dados['posicao'] = obter_dado("Posição na Linha (ex: 1, 2, 3...): ", int)

    print("\n" + "="*50)
    print("Processando dados e enviando para o Banco de Dados...")
    print("="*50)

    # A MÁGICA ACONTECE AQUI: Chamamos a sua função testada e passamos o dicionário
    sucesso, mensagem = create(dados)

    if sucesso:
        print(f"\n ✅ SUCESSO: {mensagem}")
    else:
        print(f"\n ❌ ERRO: {mensagem}")

if __name__ == "__main__":
    main()