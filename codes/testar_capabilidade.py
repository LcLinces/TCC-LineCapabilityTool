# testar_capabilidade.py
# Script de teste manual para o módulo capabilidade.py
# Não depende de banco de dados nem Flask — usa dicionários "fake".

from capability import avaliar_maquina, avaliar_linha


# ══════════════════════════════════════════════
# HELPER: imprime resultado formatado
# ══════════════════════════════════════════════
def imprimir_resultado_maquina(titulo, resultado):
    print(f"\n── {titulo} ──")
    print(f"  Status: {resultado['status']}")
    if resultado['falhas']:
        print(f"  Falhas: {resultado['falhas']}")
    if resultado['campos_ausentes']:
        print(f"  Campos ausentes: {resultado['campos_ausentes']}")


def imprimir_resultado_linha(titulo, resultado):
    print(f"\n══ {titulo} ══")
    print(f"Status da LINHA: {resultado['status']}")
    print(f"Máquinas da linha:")
    for m in resultado['maquinas']:
        print(f"  • {m['tag_maquina']} ({m['nome']}) → {m['status']}", end="")
        if m['falhas']:
            print(f"  | falhas: {m['falhas']}", end="")
        if m['campos_ausentes']:
            print(f"  | ausentes: {m['campos_ausentes']}", end="")
        print()


# ══════════════════════════════════════════════
# DADOS DE EXEMPLO
# ══════════════════════════════════════════════

# Uma máquina "ideal", com todos os limites preenchidos.
maquina_ok = {
    "tag_maquina": "M001",
    "nome": "Impressora Stencil",
    "posicao": 1,
    "min_pcb_larg_mm": 50,
    "max_pcb_larg_mm": 300,
    "min_pcb_comp_mm": 50,
    "max_pcb_comp_mm": 400,
    "max_height_limit_mm": 50,
    "max_pcb_peso_kg": 2.0,
}

# Uma máquina com limites mais apertados (vai reprovar PCBs grandes).
maquina_apertada = {
    "tag_maquina": "M002",
    "nome": "Pick & Place",
    "posicao": 2,
    "min_pcb_larg_mm": 80,
    "max_pcb_larg_mm": 200,
    "min_pcb_comp_mm": 80,
    "max_pcb_comp_mm": 250,
    "max_height_limit_mm": 30,
    "max_pcb_peso_kg": 1.0,
}

# Uma máquina com peso máximo faltando no banco (simulando NULL).
maquina_incompleta = {
    "tag_maquina": "M003",
    "nome": "Forno Reflow",
    "posicao": 3,
    "min_pcb_larg_mm": 50,
    "max_pcb_larg_mm": 350,
    "min_pcb_comp_mm": 50,
    "max_pcb_comp_mm": 400,
    "max_height_limit_mm": 60,
    "max_pcb_peso_kg": None,  # ← campo ausente
}


# ══════════════════════════════════════════════
# CENÁRIOS DE TESTE
# ══════════════════════════════════════════════

print("═══════════════════════════════════════════════════════")
print("TESTE 1: PCB pequeno e leve, deve passar na máquina OK")
print("═══════════════════════════════════════════════════════")
teste1 = {"largura": 150, "comprimento": 200, "altura": 25, "peso": 0.5}
imprimir_resultado_maquina("Máquina OK", avaliar_maquina(maquina_ok, teste1))


print("\n═══════════════════════════════════════════════════════")
print("TESTE 2: PCB grande, deve reprovar na máquina apertada")
print("═══════════════════════════════════════════════════════")
teste2 = {"largura": 280, "comprimento": 380, "altura": 40, "peso": 1.8}
imprimir_resultado_maquina("Máquina OK (aceita grande)", avaliar_maquina(maquina_ok, teste2))
imprimir_resultado_maquina("Máquina Apertada (reprova)", avaliar_maquina(maquina_apertada, teste2))


print("\n═══════════════════════════════════════════════════════")
print("TESTE 3: Máquina com peso máx. ausente → INCONCLUSIVO")
print("═══════════════════════════════════════════════════════")
teste3 = {"largura": 150, "comprimento": 200, "altura": 25, "peso": 0.5}
imprimir_resultado_maquina("Máquina Incompleta", avaliar_maquina(maquina_incompleta, teste3))


print("\n═══════════════════════════════════════════════════════")
print("TESTE 4: Valor exatamente no limite (deve passar com >=/<=)")
print("═══════════════════════════════════════════════════════")
teste4 = {"largura": 50, "comprimento": 400, "altura": 50, "peso": 2.0}
imprimir_resultado_maquina("Máquina OK nos limites exatos", avaliar_maquina(maquina_ok, teste4))


print("\n═══════════════════════════════════════════════════════")
print("TESTE 5: Linha inteira OK (todas as máquinas aprovam)")
print("═══════════════════════════════════════════════════════")
linha_toda_ok = [maquina_ok]  # só uma máquina, e ela aprova
imprimir_resultado_linha(
    "Linha com 1 máquina, PCB pequeno",
    avaliar_linha(linha_toda_ok, teste1)
)


print("\n═══════════════════════════════════════════════════════")
print("TESTE 6: Linha NOK (uma máquina reprova)")
print("═══════════════════════════════════════════════════════")
linha_mista = [maquina_ok, maquina_apertada]
imprimir_resultado_linha(
    "Linha com 2 máquinas, PCB grande",
    avaliar_linha(linha_mista, teste2)
)


print("\n═══════════════════════════════════════════════════════")
print("TESTE 7: Linha NOK por INCONCLUSIVO (regra: apenas todas-OK = OK)")
print("═══════════════════════════════════════════════════════")
linha_com_incompleta = [maquina_ok, maquina_incompleta]
imprimir_resultado_linha(
    "Linha com máquina de campo ausente",
    avaliar_linha(linha_com_incompleta, teste3)
)