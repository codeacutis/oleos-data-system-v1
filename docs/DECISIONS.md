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

---

## DEC10 — Substituição de nomes por códigos no dashboard

**Decisão**: Nomes de responsáveis e professores foram substituídos por códigos (`OB001`, `OB002`...) em todas as visualizações do dashboard.

**Motivo**: Nomes são dados pessoais sensíveis sob a LGPD. A coluna `codigo` foi adicionada à tabela `Observador` e populada com o padrão `CONCAT('OB', LPAD(id_observador, 3, '0'))`. O campo `diagnostico` também foi removido das queries por ser redundante (todos os participantes têm TEA).

---

## DEC11 — Padding de linhas no transform

**Decisão**: Antes de criar o DataFrame, cada linha de resposta é completada com strings vazias até atingir o tamanho do cabeçalho.

**Motivo**: A Google Sheets API omite células vazias do final de cada linha. Sem o padding, linhas com respostas faltantes causam `ValueError` ao criar o DataFrame com colunas fixas.

---

## DEC13 — Sono armazenado como opção categórica

**Decisão**: As queries de sono usam `CASE WHEN` sobre `Opcao_Categorica.descricao` para converter as respostas em valores numéricos antes de calcular a média.

**Motivo**: O item de sono é respondido com opções categóricas ("menos de 4h", "4h", "6h", "8h", "mais de 8h") e salvo em `id_opcao`, não em `valor_numerico`. Usar `avg(valor_numerico)` retornava sempre `NULL`. O mapeamento via `CASE WHEN` permite calcular médias significativas.

---

## DEC14 — Pasta `pages/` renomeada para `sections/`

**Decisão**: A pasta `view/pages/` foi renomeada para `view/sections/`.

**Motivo**: O Streamlit detecta automaticamente arquivos dentro de qualquer pasta chamada `pages/` e os exibe na navegação, independente do estado de autenticação. Renomear para `sections/` elimina esse comportamento e garante que as páginas só sejam acessíveis após login.

---

## DEC15 — Autenticação com login único

**Decisão**: O dashboard utiliza `streamlit-authenticator` com login único, sem RBAC. Todos os usuários autenticados têm acesso às mesmas páginas.

**Motivo**: O sistema é destinado exclusivamente a pesquisadores com perfil de consulta. Não há necessidade de controle granular de acesso. As credenciais são armazenadas em `.streamlit/secrets.toml` com senhas em hash bcrypt.

---

## DEC17 — Conexão com banco via st.secrets no dashboard

**Decisão**: O `view/db.py` conecta diretamente ao banco usando `st.secrets`, sem passar por variáveis de ambiente ou pelo `db_connection.py`.

**Motivo**: No Streamlit Community Cloud, injetar as credenciais em variáveis de ambiente antes do `@st.cache_resource` causava fallback para `localhost`. A conexão direta via `st.secrets` dentro da função garante que as credenciais do Railway sejam usadas corretamente tanto em ambiente local quanto em produção.

---

## DEC18 — Cache nos dados, não na conexão

**Decisão**: O `@st.cache_data(ttl=3600)` é aplicado na função `query_execute`, e não na conexão com o banco.

**Motivo**: Conexões MySQL têm tempo de vida limitado e podem ser encerradas pelo servidor por inatividade. Cachear a conexão com `@st.cache_resource` causava erros `MySQL Connection not available` após períodos de ociosidade. Cachear o resultado (um DataFrame) é mais seguro pois o dado não expira nem quebra. O TTL de 1 hora é adequado pois os dados só mudam quando o ETL roda.

---

## DEC19 — Pré-carregamento das queries estáticas após login

**Decisão**: A função `preload_data` no `main.py` executa todas as queries estáticas logo após o usuário ser autenticado.

**Motivo**: O Streamlit só executa o código de uma página quando o usuário a visita, causando demora na primeira visita de cada página. O pré-carregamento popula o cache compartilhado do `@st.cache_data` imediatamente após o login, tornando a navegação instantânea. Queries dinâmicas (parametrizadas por criança ou fase) não são pré-carregadas pois dependem da interação do usuário.

**Decisão**: O registro de LOGOUT na tabela `Auditoria` é feito detectando a chave `logout: true` no `session_state`, combinada com uma flag `_logout_registered` para evitar duplicatas.

**Motivo**: O `streamlit-authenticator` limpa `username` do `session_state` antes do rerun causado pelo logout, tornando impossível capturar o usuário após o evento. A solução salva o username em `_current_user` a cada render autenticado e detecta o logout pela chave interna `logout` do authenticator. A flag `_logout_registered` é resetada apenas quando `logout` não está ativo, evitando registro duplicado no rerun seguinte ao login.

---

## DEC23 — Backup local via `mysqldump` + Agendador de Tarefas

**Decisão**: O backup do banco é feito por um script `backup.py` na raiz do projeto que executa `mysqldump` e salva o dump em `backups/` (não versionado). O script é agendado via Agendador de Tarefas do Windows para rodar 30 minutos após a inicialização do sistema.

**Motivo**: O banco está no Railway, que não oferece backup automático no plano gratuito. A abordagem local é simples, sem custo adicional e sem dependência de novos serviços. O atraso de 30 minutos garante que o login do usuário já ocorreu antes da execução. Os backups não são versionados pois contêm dados sensíveis dos participantes da pesquisa. em `colors.py`

**Decisão**: Todas as cores dos gráficos do dashboard foram centralizadas no arquivo `view/colors.py`, com constantes e dicionários de mapeamento importados por cada página.

**Motivo**: Cores com significado (vermelho=negativo, verde=positivo, amarelo=atenção, cinza=referência) precisam ser consistentes em todo o dashboard. Centralizar em um único arquivo evita repetição, facilita ajustes futuros e garante que o mesmo evento (ex: resistência ao óleo) sempre aparecerá com a mesma cor em qualquer página. O arquivo expõe constantes (`VERDE`, `VERMELHO`, `AMARELO`, `LARANJA`, `AZUL`, `CINZA`), dicionários de mapeamento (`FASES`, `PERIODOS`, `SENTIMENTOS`, `AMBIENTES`, `COMPORTAMENTO`) e sequências (`SEQUENCIA_NEUTRA`, `SEQUENCIA_DOMINIOS`, `SEQUENCIA_OLEOS`).

---

## DEC22 — Rótulos curtos via `CASE WHEN LIKE` nas queries

**Decisão**: As queries `yes_no_frequency`, `yes_no_frequency_by_fase` e `yes_no_frequency_by_oil` usam `CASE WHEN descricao LIKE` para mapear descrições longas das opções categóricas para rótulos curtos diretamente no SQL.

**Motivo**: As descrições originais no banco são frases completas (ex: "Sim, houve mudança na rotina"), inadequadas para exibição em gráficos. Fazer o mapeamento no SQL evita lógica de renomeação espalhada nas páginas e mantém os DataFrames já prontos para visualização.

**Decisão**: A autenticação com a Google Sheets API foi migrada de OAuth2 (`token.json` + `client_secret.json`) para Service Account (`service_account.json`).

**Motivo**: O OAuth2 exige interação do usuário para gerar o token inicial e o token expira periodicamente, tornando o fluxo incompatível com ambientes headless como o GitHub Actions. A Service Account usa uma chave permanente que nunca expira e não requer nenhuma interação, resolvendo o travamento da pipeline.
