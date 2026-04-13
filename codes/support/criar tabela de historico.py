import sqlite3
import os

# =============================================================================
# CONFIGURAÇÕES
# =============================================================================
DB_NAME  = 'lista_maquinas.db'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH  = os.path.join(BASE_DIR, DB_NAME)

conn = None

try:
    print(f"Conectando ao banco: {DB_NAME}...")
    conn   = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    # =========================================================================
    # PASSO A — Tabela Central de Auditoria
    # =========================================================================
    print("Criando tabela de auditoria...")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS auditoria (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        tabela      TEXT NOT NULL,
        operacao    TEXT NOT NULL,
        tag_maquina TEXT,
        data_hora   TEXT DEFAULT (datetime('now', 'localtime')),
        detalhes    TEXT
    );""")

    # =========================================================================
    # PASSO B — Triggers: maquinas
    # =========================================================================
    print("Criando triggers para 'maquinas'...")

    cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS trg_audit_maquinas_insert
    AFTER INSERT ON maquinas
    BEGIN
        INSERT INTO auditoria (tabela, operacao, tag_maquina, detalhes)
        VALUES ('maquinas', 'INSERT', NEW.tag_maquina,
            'nome: '  || COALESCE(NEW.nome_maquina, '-') ||
            ' | tipo: '|| COALESCE(NEW.tipo, '-'));
    END;""")

    cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS trg_audit_maquinas_update
    AFTER UPDATE ON maquinas
    BEGIN
        INSERT INTO auditoria (tabela, operacao, tag_maquina, detalhes)
        VALUES ('maquinas', 'UPDATE', NEW.tag_maquina,
            'nome: '  || COALESCE(NEW.nome_maquina, '-') ||
            ' | tipo: '|| COALESCE(NEW.tipo, '-'));
    END;""")

    cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS trg_audit_maquinas_delete
    AFTER DELETE ON maquinas
    BEGIN
        INSERT INTO auditoria (tabela, operacao, tag_maquina, detalhes)
        VALUES ('maquinas', 'DELETE', OLD.tag_maquina,
            'nome: '  || COALESCE(OLD.nome_maquina, '-') ||
            ' | tipo: '|| COALESCE(OLD.tipo, '-'));
    END;""")

    # =========================================================================
    # PASSO C — Triggers: espec_maquinas
    # =========================================================================
    print("Criando triggers para 'espec_maquinas'...")

    cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS trg_audit_espec_insert
    AFTER INSERT ON espec_maquinas
    BEGIN
        INSERT INTO auditoria (tabela, operacao, tag_maquina, detalhes)
        VALUES ('espec_maquinas', 'INSERT', NEW.tag_maquina,
            'max_comp: ' || COALESCE(NEW.max_pcb_comp_mm, '-') ||
            ' | max_larg: '|| COALESCE(NEW.max_pcb_larg_mm, '-') ||
            ' | max_alt: '  || COALESCE(NEW.max_height_limit_mm, '-'));
    END;""")

    cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS trg_audit_espec_update
    AFTER UPDATE ON espec_maquinas
    BEGIN
        INSERT INTO auditoria (tabela, operacao, tag_maquina, detalhes)
        VALUES ('espec_maquinas', 'UPDATE', NEW.tag_maquina,
            'max_comp: ' || COALESCE(NEW.max_pcb_comp_mm, '-') ||
            ' | max_larg: '|| COALESCE(NEW.max_pcb_larg_mm, '-') ||
            ' | max_alt: '  || COALESCE(NEW.max_height_limit_mm, '-'));
    END;""")

    cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS trg_audit_espec_delete
    AFTER DELETE ON espec_maquinas
    BEGIN
        INSERT INTO auditoria (tabela, operacao, tag_maquina, detalhes)
        VALUES ('espec_maquinas', 'DELETE', OLD.tag_maquina,
            'max_comp: ' || COALESCE(OLD.max_pcb_comp_mm, '-') ||
            ' | max_larg: '|| COALESCE(OLD.max_pcb_larg_mm, '-') ||
            ' | max_alt: '  || COALESCE(OLD.max_height_limit_mm, '-'));
    END;""")

    # =========================================================================
    # PASSO D — Triggers: dim_maquinas
    # =========================================================================
    print("Criando triggers para 'dim_maquinas'...")

    cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS trg_audit_dim_insert
    AFTER INSERT ON dim_maquinas
    BEGIN
        INSERT INTO auditoria (tabela, operacao, tag_maquina, detalhes)
        VALUES ('dim_maquinas', 'INSERT', NEW.tag_maquina,
            'comp: ' || COALESCE(NEW.comp_maquina, '-') ||
            ' | larg: '|| COALESCE(NEW.larg_maquina, '-') ||
            ' | alt: ' || COALESCE(NEW.alt_maquina, '-'));
    END;""")

    cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS trg_audit_dim_update
    AFTER UPDATE ON dim_maquinas
    BEGIN
        INSERT INTO auditoria (tabela, operacao, tag_maquina, detalhes)
        VALUES ('dim_maquinas', 'UPDATE', NEW.tag_maquina,
            'comp: ' || COALESCE(NEW.comp_maquina, '-') ||
            ' | larg: '|| COALESCE(NEW.larg_maquina, '-') ||
            ' | alt: ' || COALESCE(NEW.alt_maquina, '-'));
    END;""")

    cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS trg_audit_dim_delete
    AFTER DELETE ON dim_maquinas
    BEGIN
        INSERT INTO auditoria (tabela, operacao, tag_maquina, detalhes)
        VALUES ('dim_maquinas', 'DELETE', OLD.tag_maquina,
            'comp: ' || COALESCE(OLD.comp_maquina, '-') ||
            ' | larg: '|| COALESCE(OLD.larg_maquina, '-') ||
            ' | alt: ' || COALESCE(OLD.alt_maquina, '-'));
    END;""")

    # =========================================================================
    # PASSO E — Triggers: linha
    # =========================================================================
    print("Criando triggers para 'linha'...")

    cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS trg_audit_linha_insert
    AFTER INSERT ON linha
    BEGIN
        INSERT INTO auditoria (tabela, operacao, tag_maquina, detalhes)
        VALUES ('linha', 'INSERT', NEW.tag_maquina,
            'linha: '    || COALESCE(NEW.linha, '-') ||
            ' | posicao: '|| COALESCE(NEW.posicao, '-'));
    END;""")

    cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS trg_audit_linha_update
    AFTER UPDATE ON linha
    BEGIN
        INSERT INTO auditoria (tabela, operacao, tag_maquina, detalhes)
        VALUES ('linha', 'UPDATE', NEW.tag_maquina,
            'linha: '    || COALESCE(NEW.linha, '-') ||
            ' | posicao: '|| COALESCE(NEW.posicao, '-'));
    END;""")

    cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS trg_audit_linha_delete
    AFTER DELETE ON linha
    BEGIN
        INSERT INTO auditoria (tabela, operacao, tag_maquina, detalhes)
        VALUES ('linha', 'DELETE', OLD.tag_maquina,
            'linha: '    || COALESCE(OLD.linha, '-') ||
            ' | posicao: '|| COALESCE(OLD.posicao, '-'));
    END;""")

    # =========================================================================
    # COMMIT FINAL
    # =========================================================================
    conn.commit()
    print("\n✔ Tabela de auditoria e triggers criados com sucesso!")

except Exception as e:
    print(f"\n✘ Erro crítico: {e}")

finally:
    if conn:
        conn.close()
        print("  Conexão encerrada com segurança.")