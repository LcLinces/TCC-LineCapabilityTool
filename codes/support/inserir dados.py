import pandas as pd
import sqlite3

"""
df = pd.read_excel('dados_maquinas.xlsx')

colunas_desejadas = [
  'tag_maquina',
  'serial_No',
  'nome_maquina',
  'tipo',
  'tensao_v',
  'frequencia_hz',
  'potencia',
  'unidade_potencia',
  'pressao',
  'unidade_pressao'
]   
"""
df = pd.read_excel('dados_maquinas.xlsx')

colulnas = [
    'tag_maquina',
    'max_pcb_peso_kg',
    'min_pcb_comp_mm', 
    'min_pcb_larg_mm',
    'max_pcb_comp_mm',
    'max_pcb_larg_mm',
    'max_height_limit_mm',
    'Fixture'
]

# 2. Conectar ao Banco
conn = sqlite3.connect('lista_maquinas.db')

# 3. Inserir no Banco
try:
    # if_exists='append': Adiciona os dados sem apagar o que já existe
    # index=False: Não cria uma coluna extra para o número da linha do Excel
    df_excel = pd.read_excel('dados_maquinas.xlsx', usecols=colulnas)
    
# Inserir no Banco
    df_excel.to_sql('espec_maquinas', conn, if_exists='append', index=False)
    
# Filtro para passar apenas dados inexistentes  
# Passo A: Perguntar ao banco quais Tags ele JÁ TEM
    try:
        df_banco = pd.read_sql("SELECT tag_maquina FROM espec_maquinas", conn)
        tags_existentes = df_banco['tag_maquina'].tolist()
    except:
        # Se a tabela ainda não existir (primeira vez), a lista é vazia
        tags_existentes = []

    # Passo B: Filtrar o Excel
    # Mantém apenas as linhas onde 'tag_maquina' NÃO ESTÁ (~) na lista de existentes
    df_para_inserir = df_excel[~df_excel['tag_maquina'].isin(tags_existentes)]
    
    # 5. Inserir (Se houver algo novo)
    if not df_para_inserir.empty:
        df_para_inserir.to_sql('maquinas', conn, if_exists='append', index=False)
        print(f"Sucesso! {len(df_para_inserir)} NOVAS máquinas foram cadastradas.")
    else:
        print("Nenhuma alteração necessária. Todas as máquinas do Excel já estão no banco.")

    conn.close()

except Exception as e:
    print(f"Erro: {e}")