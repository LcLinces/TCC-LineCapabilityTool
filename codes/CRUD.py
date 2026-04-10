import sqlite3
import os

DB_NAME = 'lista_maquinas.db'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, DB_NAME)

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


# CREATE - criação de nova máquina no banco de dados

def create(dados):
    conn = get_conn()
    cursor = conn.cursor()

    try:
        # 1. Insere na Tabela MÃE primeiro
        cursor.execute("""
            INSERT INTO maquinas (tag_maquina, serial_No, nome_maquina, tipo, tensao_v, frequencia_hz, potencia, unidade_potencia, pressao, unidade_pressao, comentario)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (dados['tag_maquina'], dados.get('serial_No'), dados['nome_maquina'], dados['tipo'], 
              dados.get('tensao_v'), dados.get('frequencia_hz'), dados.get('potencia'), 
              dados.get('unidade_potencia'), dados.get('pressao'), dados.get('unidade_pressao'), dados.get('comentario')))

        # 2. Insere nas Tabelas FILHAS
        cursor.execute("""
            INSERT INTO espec_maquinas (tag_maquina, max_pcb_peso_kg, min_pcb_comp_mm, min_pcb_larg_mm, max_pcb_comp_mm, max_pcb_larg_mm, max_height_limit_mm)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (dados['tag_maquina'], dados.get('max_pcb_peso_kg'), dados.get('min_pcb_comp_mm'), 
              dados.get('min_pcb_larg_mm'), dados.get('max_pcb_comp_mm'), dados.get('max_pcb_larg_mm'), dados.get('max_height_limit_mm')))

        cursor.execute("""
            INSERT INTO dim_maquinas (tag_maquina, peso_maquina, comp_maquina, larg_maquina, alt_maquina)
            VALUES (?, ?, ?, ?, ?)
        """, (dados['tag_maquina'], dados.get('peso_maquina'), dados.get('comp_maquina'), 
              dados.get('larg_maquina'), dados.get('alt_maquina')))

        cursor.execute("""
            INSERT INTO linha (tag_maquina, linha, posicao)
            VALUES (?, ?, ?)
        """, (dados['tag_maquina'], dados.get('linha'), dados.get('posicao')))

        conn.commit() # Confirma tudo se nada deu errado
        return True, "Máquina cadastrada com sucesso."

    except sqlite3.IntegrityError as e:
        conn.rollback() # Desfaz TUDO se der erro (ex: Tag já existe)
        return False, f"Erro de integridade: A TAG já existe ou dados inválidos. ({e})"
    except Exception as e:
        conn.rollback()
        return False, f"Erro inesperado: {e}"
    finally:
        conn.close()