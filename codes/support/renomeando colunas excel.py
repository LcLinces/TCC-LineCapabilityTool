import pandas as pd 
import sqlite3

# 1. Carregar a planilha
df = pd.read_excel('dados_maquinas.xlsx')

# 2. Renomear colunas
# Como os dados vêm de uma planilha do excel, é importante que as colunas estejam com o mesmo nome
df = df.rename(columns={
    'TAG': 'tag_maquina',
    'Serial No.': 'serial_No',
    'MACHINE': 'nome_maquina',
    'TYPE': 'tipo',
    'VOLTAGE': 'tensao_v',
    'FREQUENCY': 'frequencia_hz',
    'POWER': 'potencia',
    'UNIDADE_POT': 'unidade_potencia',
    'PRESSURE': 'pressao',
    'UNIDADE PRESS': 'unidade_pressao',
    'Max PCB Weight (Kg)':'max_pcb_peso_kg',
    'Min PCB L (mm)':'min_pcb_comp_mm', 
    'Min PCB W (mm)':'min_pcb_larg_mm',
    'Max PCB L (mm)':'max_pcb_comp_mm',
    'Max PCB W (mm)':'max_pcb_larg_mm',
    'Max Height Limit (mm)':'max_height_limit_mm',
    'Machine Weigth (Kg)':'peso_maquina',
    'Machine Length (mm)':'comp_maquina',
    'Machine Width (mm)':'larg_maquina',
    'Machine Heigth (mm)':'alt_maquina',
    'LINE':'linha',
    'POSITION':'posicao',
    'COMENT':'comentario',

})

# 4. Salvar as alterações no disco (AQUI ESTÁ O SEGREDO)
# index=False impede que o Pandas crie uma coluna extra com números (0, 1, 2...)
try:
    df.to_excel('dados_maquinas.xlsx', index=False)
    print("Sucesso! A planilha foi atualizada e salva.")
except PermissionError:
    print("ERRO: Feche o arquivo Excel antes de rodar o script!")
    print("O Python não consegue salvar se o arquivo estiver aberto no Excel.")
