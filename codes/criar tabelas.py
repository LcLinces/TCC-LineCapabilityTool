import sqlite3

conn = sqlite3.connect('lista_maquinas.db') #busca esse arquivo banco de dados na pasta aberta no momento.
cursor = conn.cursor()


cursor.execute("PRAGMA foreign_keys = ON;") # Habilita chaves estrangeiras

sql_create_table = """
CREATE TABLE espec_maquinas (
    tag_maquina TEXT PRIMARY KEY,
    max_pcb_peso_kg REAL,
    min_pcb_comp_mm REAL,
    min_pcb_larg_mm REAL,
    max_pcb_comp_mm REAL,
    max_pcb_larg_mm REAL,
    max_height_limit_mm REAL,
    fixture BOOLEAN,

    CONSTRAINT fk_limites_maquina
        FOREIGN KEY (tag_maquina) 
        REFERENCES maquinas_info_geral(tag_maquina) 
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
"""


cursor.execute(sql_create_table)
    
# Confirmar as alterações (Commit)
conn.commit()
print("Sucesso! Tabela 'espec_maquinas' criada corretamente.")