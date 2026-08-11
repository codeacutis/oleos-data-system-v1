# Decisões Técnicas

Registro das principais decisões tomadas ao longo do desenvolvimento e suas justificativas.

---

## DEC01 — IDs hardcoded no seed.py

**Decisão**: As funções `observer_child_insert()` e demais funções de seed utilizam IDs hardcoded em vez de buscá-los dinamicamente.

**Motivo**: Os dados estáticos do estudo (crianças, observadores, fases, óleos) são conhecidos e fixos. O uso de IDs hardcoded é intencional e consistente com o padrão do projeto, simplificando a população inicial do banco sem perda de confiabilidade.

---

## DEC02 — get_id_opcao retorna None intencionalmente

**Decisão**: A função `get_id_opcao` no `database_loader.py` retorna `None` quando a opção não é encontrada, em vez de lançar `ValueError` como as demais funções `get_*`.

**Motivo**: Nem todas as respostas possuem `id_opcao`. Respostas numéricas, de texto e de sono não utilizam esse campo. Retornar `None` permite que a carga continue normalmente nesses casos.

---

## DEC03 — Separação de Observador e Observador_Crianca

**Decisão**: A relação entre observador e criança foi movida para uma tabela associativa `Observador_Crianca`, removendo `id_crianca` e `ambiente` diretamente de `Observador`.

**Motivo**: Um observador pode estar associado a mais de uma criança. A tabela associativa permite essa flexibilidade e mantém a integridade referencial.

---

## DEC04 — Formulario.tipo usa ENUM PAIS/PROFESSOR

**Decisão**: O campo `tipo` da tabela `Formulario` usa os valores `'PAIS'` e `'PROFESSOR'`, enquanto `Observador.tipo` usa `'RESPONSAVEL'` e `'PROFESSOR'`.

**Motivo**: Os formulários foram nomeados antes da padronização do sistema. O `config.yaml` usa `'RESPONSAVEL'` para identificar o tipo do observador no ETL, e o mapeamento é feito no `app.py`.

---

## DEC05 — @st.cache_resource na conexão do banco

**Decisão**: A função `connection()` no `view/db.py` utiliza o decorator `@st.cache_resource`.

**Motivo**: Evita que uma nova conexão com o banco seja criada a cada rerun do Streamlit, melhorando o desempenho e evitando esgotamento de conexões.

---

## DEC06 — sys.path configurado manualmente em cada página

**Decisão**: Cada arquivo dentro de `view/pages/` insere manualmente o caminho da raiz no `sys.path` antes dos imports.

**Motivo**: O Streamlit executa cada página como um script independente, sem herdar o contexto de execução do `main.py`. A configuração manual garante que os módulos do projeto sejam encontrados corretamente.

---

## DEC07 — Queries dinâmicas como funções no queries.py

**Decisão**: Queries que recebem parâmetros (como código da criança ou fase) são implementadas como funções no `queries.py`, enquanto queries estáticas ficam no dicionário `queries`.

**Motivo**: Separa claramente queries fixas de queries parametrizadas, mantendo o código das páginas limpo e centralizando a lógica SQL em um único arquivo.

---

## DEC08 — Atributo regular na tabela Crianca

**Decisão**: Foi adicionado o atributo `regular` com ENUM `'MANHÃ'/'TARDE'` na tabela `Crianca`.

**Motivo**: Crianças com turno `INTEGRAL` precisam ter seu turno de ensino regular identificado para permitir comparações entre grupos. Crianças com turno `MANHÃ` ou `TARDE` têm `regular` com o mesmo valor do turno.

---

## DEC09 — Linha de base excluída das comparações por óleo

**Decisão**: As análises de comparação entre óleos essenciais excluem automaticamente a fase de linha de base.

**Motivo**: A linha de base não possui óleo associado (`id_oleo = NULL`). O uso de `INNER JOIN` com a tabela `Oleo` garante a exclusão automática dessa fase nas queries relevantes.
