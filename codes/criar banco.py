import sqlite3
import pandas as pd
import os

# 1. Configurações de Diretório
DB_NAME = 'lista_maquinas.db'
EXCEL_FILE = 'dados_maquinas.xlsx'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, DB_NAME)
EXCEL_PATH = os.path.join(BASE_DIR, EXCEL_FILE)

# 2. Listas de Colunas (Exatamente como estão no seu Excel)
colunas_maquinas = [
    'tag_maquina', 'serial_No', 'nome_maquina', 'tipo', 'tensao_v', 
    'frequencia_hz', 'potencia', 'unidade_potencia', 'pressao', 
    'unidade_pressao', 'comentario'
]
colunas_espec = [
    'tag_maquina', 'max_pcb_peso_kg', 'min_pcb_comp_mm', 
    'min_pcb_larg_mm', 'max_pcb_comp_mm', 'max_pcb_larg_mm', 
    'max_height_limit_mm'
]
colunas_dim = [
    'tag_maquina', 'peso_maquina', 
    'comp_maquina', 'larg_maquina', 'alt_maquina'
]
colunas_linha = [
    'tag_maquina', 'linha', 'posicao'
]

# --- INÍCIO DO CÓDIGO SEGURO ---
conn = None # Inicializa a variável como vazia para não dar erro no finally

try:
    print(f"Criando e conectando ao banco: {DB_NAME}...")
    
    # É AQUI QUE O SEU CÓDIGO ESTAVA FALHANDO!
    # Estas duas linhas não podem faltar:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("PRAGMA foreign_keys = ON;")

    # --- PASSO A: Criação das Tabelas (DDL) ---
    print("Construindo arquitetura de tabelas...")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS maquinas (
        tag_maquina CHAR[10] PRIMARY KEY, serial_No CHAR[20], nome_maquina CHAR[50], tipo CHAR [20],
        tensao_v REAL, frequencia_hz REAL, potencia REAL, unidade_potencia CHAR[6],
        pressao REAL, unidade_pressao CHAR[6], comentario TEXT
    );""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS espec_maquinas (
        tag_maquina CHAR[10] PRIMARY KEY, max_pcb_peso_kg NUMERIC(4,2), min_pcb_comp_mm NUMERIC(4,2),
        min_pcb_larg_mm NUMERIC(4,2), max_pcb_comp_mm NUMERIC(4,2), max_pcb_larg_mm NUMERIC(4,2), max_height_limit_mm REAL,
        CONSTRAINT fk_espec FOREIGN KEY (tag_maquina) REFERENCES maquinas(tag_maquina) ON DELETE CASCADE
    );""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dim_maquinas (
        tag_maquina CHAR[10] PRIMARY KEY, peso_maquina NUMERIC(4,2),
        comp_maquina NUMERIC(4,2), larg_maquina NUMERIC(4,2), alt_maquina NUMERIC(4,2),
        CONSTRAINT fk_dim FOREIGN KEY (tag_maquina) REFERENCES maquinas(tag_maquina) ON DELETE CASCADE
    );""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS linha (
        tag_maquina CHAR[10] PRIMARY KEY, linha INTEGER, posicao INTEGER,
        CONSTRAINT fk_linha FOREIGN KEY (tag_maquina) REFERENCES maquinas(tag_maquina) ON DELETE CASCADE
    );""")
    conn.commit()

    # --- PASSO B: Função de Carga Incremental ---
    def inserir_dados(lista_colunas, nome_tabela):
        df = pd.read_excel(EXCEL_PATH, usecols=lista_colunas)
        df = df.dropna(subset=['tag_maquina'])
        
        try:
            tags_banco = pd.read_sql(f"SELECT tag_maquina FROM {nome_tabela}", conn)['tag_maquina'].tolist()
        except:
            tags_banco = []
            
        df_novo = df[~df['tag_maquina'].isin(tags_banco)]
        
        if not df_novo.empty:
            df_novo.to_sql(nome_tabela, conn, if_exists='append', index=False)
            print(f" -> {len(df_novo)} registros salvos em '{nome_tabela}'.")
        else:
            print(f" -> Tabela '{nome_tabela}' já está atualizada.")

    # --- PASSO C: Execução da Carga ---
    print("Iniciando importação dos dados...")
    inserir_dados(colunas_maquinas, 'maquinas')
    inserir_dados(colunas_espec, 'espec_maquinas')
    inserir_dados(colunas_dim, 'dim_maquinas')
    inserir_dados(colunas_linha, 'linha')

    print("\nProcesso concluído com sucesso! Banco de dados estruturado e populado.")

except Exception as e:
    print(f"\nErro Crítico: {e}")

finally:
    # Só tenta fechar se a conexão realmente existir
    if conn:
        conn.close()
        print("Conexão fechada com segurança.")