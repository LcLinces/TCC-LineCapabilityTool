# Line Capability Tool

Aplicação web para gerenciamento de máquinas industriais em ambiente de manufatura, organizadas por linha de produção e tipo. Projeto desenvolvido como TCC (Trabalho de Conclusão de Curso).

## Stack

- **Backend:** Flask (Python)
- **Frontend:** HTML + Bootstrap 4.6 (via CDN) + JavaScript vanilla
- **Banco de dados:** SQLite
- **Camada de dados:** módulo `db.py` com funções CRUD
- **Referência visual:** protótipo existente em Power Apps

## Arquitetura

A aplicação é uma **single-page dynamic app**. Não há recarregamento de página entre ações — o painel de detalhes é atualizado via `fetch()` para endpoints de API do Flask, que retornam JSON. Houve uma migração consciente saindo de uma abordagem multi-página com `detalhes.html` separado; **não voltar** a esse modelo.

### Layout

- **Barra superior fixa:** filtro + botões de modo (`VER`, `EDITAR`, `NOVO`, `EXCLUIR`)
- **Sidebar esquerda:** cards de máquinas (ícone + nome)
- **Painel direito:** detalhes da máquina selecionada, renderizado dinamicamente conforme o modo ativo

### Fluxo pós-save

1. App retorna automaticamente ao modo `VER`
2. Painel de detalhes é re-renderizado via `selecionarMaquina()`
3. Alerta de sucesso aparece e desaparece sozinho após **3 segundos**

### Ícones das máquinas

Atualmente são placeholders: `div` verde com a tag `<img>` comentada. A configuração final virá de uma pasta de ícones organizada por tipo de máquina — manter o placeholder até que essa pasta esteja definida.

## Convenções importantes

### Ordem de rotas no Flask (crítico)

Rotas **estáticas** devem vir **antes** das rotas **dinâmicas** em `app.py`. Caso contrário, o Flask captura tudo na rota dinâmica e quebra os endpoints específicos.

```python
# CORRETO
@app.route('/api/maquina/nova', methods=['POST'])   # estática primeiro
@app.route('/api/maquina/<tag>', methods=['GET'])   # dinâmica depois

# ERRADO — /api/maquina/nova nunca seria atingida
@app.route('/api/maquina/<tag>', methods=['GET'])
@app.route('/api/maquina/nova', methods=['POST'])
```

### Comparação de tipos no SQLite

O campo `linha` é armazenado como **inteiro** no SQLite. Valores vindos de `<select>` HTML chegam como **string**. Sempre converter com `Number()` no JavaScript antes de comparar/filtrar:

```javascript
const linhaSelecionada = Number(selectLinha.value);
const filtradas = maquinas.filter(m => m.linha === linhaSelecionada);
```

Comparar string com inteiro silenciosamente retorna lista vazia — esse bug já apareceu antes.

### Importação do módulo de banco

O arquivo CRUD pode estar nomeado de outra forma localmente. Padronizar como `db.py` ou ajustar o `import` em `app.py` conforme o nome real do arquivo. Não assumir.

### Delete com cascade

A função de delete em `db.py` depende de `ON DELETE CASCADE` estar definido no schema do banco. Antes de mexer em delete, **verificar o schema** — se o cascade não estiver lá, registros relacionados ficam órfãos.

## Como o Luis prefere trabalhar

- **Iterativamente, linha a linha / bloco a bloco.** Antes de avançar, ele quer entender o código gerado. Explicar o que cada trecho faz antes de seguir para o próximo.
- **Arquivos completos > snippets parciais.** Quando há várias mudanças acumuladas em um arquivo, entregar o conteúdo completo. Edits parciais já causaram erros antes (linhas faltando, contexto perdido).
- Manter o tom técnico e direto, sem encher de comentários óbvios no código.

## O que evitar

- Reintroduzir `detalhes.html` ou qualquer fluxo multi-página
- Adicionar dependências de frontend além de Bootstrap 4.6 sem discutir antes
- Trocar SQLite ou Bootstrap por outras stacks
- Usar versões mais novas do Bootstrap (5.x quebra classes 4.6)
- Inverter a ordem de rotas estáticas/dinâmicas no Flask
