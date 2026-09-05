# Tarefa Atual

## Estado do Desenvolvimento

### ✅ Concluído

#### ETL
- Autenticação com Google via Service Account (headless, sem interação do usuário)
- Extração dos dados via Google Sheets API (com retry em HttpError)
- Transformação e padronização dos dados
- Carga no banco MySQL (Railway)
- Tratamento de erros nas funções `get_*` do `database_loader.py`
- Correção de linhas com colunas faltantes via padding (`transform_data.py`)
- Conversão de data do formato brasileiro para `YYYY-MM-DD` no transform
- Correção de ambiguidade de `id_observador` no JOIN de `get_id_observer`
- Normalização de underscores para espaços em `get_id_item`
- Contador de inserções acumulado corretamente em `database_loader.py`
- GitHub Actions configurado para ETL diário (00:35 UTC)

#### Banco de Dados
- Modelagem completa do banco `db_oleos`
- População estática via `seed.py` (crianças, observadores, fases, óleos, itens, opções)
- Atributos `turno` e `regular` adicionados à tabela `Crianca`
- Coluna `codigo` adicionada à tabela `Observador` (formato `OB001`, `OB002`...)

#### Segurança e Privacidade
- Remoção do campo `diagnostico` das queries do dashboard
- Substituição de nomes de responsáveis e professores por códigos (`OB001`...)
- Autenticação com `streamlit-authenticator` implementada no dashboard
- Credenciais armazenadas em `.streamlit/secrets.toml` (não versionado)
- Navegação e páginas protegidas por login
- Rate limiting: bloqueio após 5 tentativas de login falhas
- Proteção contra SQL Injection via queries parametrizadas
- Auditoria de acesso: registro de LOGIN, LOGIN_FALHA e LOGOUT na tabela `Auditoria`

#### Dashboard — Visão Geral (`general.py`)
- Métricas: total de crianças, responsáveis e professores
- Gráfico de barras: crianças por turno
- Gráfico de barras: registros por fase com 4 faixas de cor semântica, linha de meta tracejada (`META = 99`) e 3 métricas abaixo
- Gráfico de pizza: crianças por fase
- Linha do tempo de registros
- Condicional de dados vazios em todos os gráficos
- Cores semânticas aplicadas via `view/colors.py`

#### Dashboard — Análise por Criança (`children.py`)
- Seletor de criança por código
- Resumo: código, idade, turno, regular, professor (código), responsável (código)
- Gráfico de barras: média por item — apenas itens ESCALA_0_4 de professores
- Gráfico de linha: evolução do sono por fase
- Gráfico de barras: frequência de eventos adversos por fase com cores semânticas
- Tabela: comportamento ao ir e voltar da escola por fase
- Condicional de dados vazios em todos os gráficos
- Cores semânticas aplicadas via `view/colors.py`

#### Dashboard — Comparações (`comparisons.py`)
- Gráfico de barras: média por turno/regular agrupada por fase
- Gráfico de radar: comparação entre duas crianças por domínio
- Comparação entre óleos essenciais (scores por domínio + dados dos pais)
- Comparação linha de base vs intervenção
- Comparação entre ambientes (domiciliar vs escolar)
- Condicional de dados vazios em todos os gráficos
- Cores semânticas aplicadas em todos os gráficos via `view/colors.py`

#### Dashboard — Adesão e Qualidade (`registers.py`)
- Adesão ao protocolo por responsável e fase (código do observador)
- Sentimento dos responsáveis: frequência e distribuição por fase + comparativo entre fases com `color_discrete_map=SENTIMENTOS`
- Frequência de resistência ao óleo por fase (vermelho)
- Frequência de mudanças na rotina por fase (amarelo)
- Condicional de dados vazios em todos os gráficos
- Cores semânticas aplicadas via `view/colors.py`

#### Backup
- Script `backup.py` na raiz do projeto
- Dump SQL via `mysqldump` salvo em `backups/db_oleos_YYYY-MM-DD_HH-MM-SS.sql`
- Pasta `backups/` no `.gitignore` (não versionada)
- Agendado via Agendador de Tarefas do Windows — executa 30 minutos após a inicialização do sistema

---

### 🔄 Em Andamento

---

## Próximo Passo

Fase 3 — Finalizar deploy:
- Mecanismo de backup

---

## Arquivos Ativos

- `view/main.py` — autenticação e auditoria implementadas
- `view/db.py` — conexão via `st.secrets`
- `view/queries.py` — queries padronizadas para minúsculo; rótulos curtos via `CASE WHEN LIKE`
- `view/colors.py` — paleta semântica centralizada
- `view/sections/general.py` — gráfico de questionários com faixas e meta
- `view/sections/children.py` — cores semânticas em eventos adversos
- `view/sections/comparisons.py` — cores semânticas em todos os gráficos
- `view/sections/registers.py` — cores semânticas em sentimentos, resistência e rotina
- `load/db_connection.py` — conexão via variáveis de ambiente (ETL local)
- `requirements.txt` — plotly adicionado
