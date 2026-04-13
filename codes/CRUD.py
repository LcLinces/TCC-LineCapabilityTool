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

        posicao = dados.get('posicao')
        nome_linha = dados.get('linha')

        # Se o usuário NÃO digitou posição, mas digitou uma linha
        if not posicao and nome_linha:
            # Busca o valor máximo da posição naquela linha específica
            resultado = cursor.execute(
                "SELECT MAX(posicao) FROM linha WHERE linha = ?", 
                (nome_linha,)
            ).fetchone()
            
            max_pos = resultado[0] # Pega o valor do MAX
            
            if max_pos is not None:
                posicao = max_pos + 1
            else:
                posicao = 1 # Se a linha for nova/vazia, começa em 1

        # Agora sim, fazemos o INSERT usando a posição calculada acima!
        cursor.execute("""
            INSERT INTO linha (tag_maquina, linha, posicao)
            VALUES (?, ?, ?)
        """, (dados['tag_maquina'], nome_linha, posicao))
        # ==============================================================

        conn.commit() # Confirma tudo se nada deu errado
        
        # Retorna a mensagem já dizendo em qual posição a máquina ficou
        return True, f"Máquina cadastrada com sucesso na posição {posicao}."

    except sqlite3.IntegrityError as e:
        conn.rollback() # Desfaz TUDO se der erro (ex: Tag já existe)
        return False, f"Erro de integridade: A TAG já existe ou dados inválidos. ({e})"
    except Exception as e:
        conn.rollback()
        return False, f"Erro inesperado: {e}"
    finally:
        conn.close()

#____________________________________________________________________________________________
# ==========================================
# READ - LEITURA DE DADOS
# ==========================================

def buscar_todas_maquinas_resumo():
    """
    Busca um resumo (Tag, Nome, Tipo e Linha) para preencher a tabela inicial do site.
    Usa LEFT JOIN para mostrar a máquina mesmo que ela ainda não esteja em nenhuma linha.
    """
    conn = get_conn()
    try:
        query = """
            SELECT m.tag_maquina, m.nome_maquina, m.tipo, l.linha, l.posicao
            FROM maquinas m
            LEFT JOIN linha l ON m.tag_maquina = l.tag_maquina
            ORDER BY l.linha, l.posicao
        """
        resultado = conn.execute(query).fetchall()
        return [dict(row) for row in resultado] # Converte para lista de dicionários
    except Exception as e:
        print(f"Erro ao buscar resumo: {e}")
        return []
    finally:
        conn.close()

def buscar_maquina_completa(tag_maquina):
    """
    Faz um LEFT JOIN gigante para buscar ABSOLUTAMENTE TUDO sobre uma máquina.
    Perfeito para a tela de 'Ver Detalhes' ou para preencher o formulário de 'Editar'.
    """
    conn = get_conn()
    try:
        query = """
            SELECT m.*, 
                   e.max_pcb_peso_kg, e.min_pcb_comp_mm, e.min_pcb_larg_mm, e.max_pcb_comp_mm, e.max_pcb_larg_mm, e.max_height_limit_mm,
                   d.peso_maquina, d.comp_maquina, d.larg_maquina, d.alt_maquina,
                   l.linha, l.posicao
            FROM maquinas m
            LEFT JOIN espec_maquinas e ON m.tag_maquina = e.tag_maquina
            LEFT JOIN dim_maquinas d ON m.tag_maquina = d.tag_maquina
            LEFT JOIN linha l ON m.tag_maquina = l.tag_maquina
            WHERE m.tag_maquina = ?
        """
        resultado = conn.execute(query, (tag_maquina,)).fetchone()
        return dict(resultado) if resultado else None
    except Exception as e:
        print(f"Erro ao buscar detalhes: {e}")
        return None
    finally:
        conn.close()