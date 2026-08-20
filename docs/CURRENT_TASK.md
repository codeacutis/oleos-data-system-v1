# Tarefa Atual

## Estado do Desenvolvimento

### ✅ Concluído

#### ETL
- Autenticação com Google OAuth2
- Extração dos dados via Google Sheets API (com retry em HttpError)
- Transformação e padronização dos dados
- Carga no banco MySQL
- Tratamento de erros nas funções `get_*` do `database_loader.py`
- Correção de linhas com colunas faltantes via padding (`transform_data.py`)
- Conversão de data do formato brasileiro para `YYYY-MM-DD` no transform
- Correção de ambiguidade de `id_observador` no JOIN de `get_id_observer`
- Normalização de underscores para espaços em `get_id_item`

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

#### Dashboard — Visão Geral (`general.py`)
- Métricas: total de crianças, responsáveis e professores
- Gráfico de barras: crianças por turno
- Gráfico de barras: registros por fase
- Gráfico de pizza: crianças por fase
- Linha do tempo de registros
- Condicional de dados vazios em todos os gráficos

#### Dashboard — Análise por Criança (`children.py`)
- Seletor de criança por código
- Resumo: código, idade, turno, regular, professor (código), responsável (código)
- Gráfico de barras: média por item — apenas itens ESCALA_0_4 de professores
- Gráfico de linha: evolução do sono por fase
- Gráfico de barras: frequência de eventos adversos por fase
- Tabela: comportamento ao ir e voltar da escola por fase
- Condicional de dados vazios em todos os gráficos

#### Dashboard — Comparações (`comparisons.py`)
- Gráfico de barras: média por turno/regular agrupada por fase
- Gráfico de radar: comparação entre duas crianças por domínio
- Comparação entre óleos essenciais (scores por domínio + dados dos pais)
- Comparação linha de base vs intervenção
- Comparação entre ambientes (domiciliar vs escolar)
- Condicional de dados vazios em todos os gráficos

#### Dashboard — Adesão e Qualidade (`registers.py`)
- Adesão ao protocolo por responsável e fase (código do observador)
- Sentimento dos responsáveis: frequência e distribuição por fase + comparativo entre fases
- Frequência de resistência ao óleo por fase
- Frequência de mudanças na rotina por fase
- Condicional de dados vazios em todos os gráficos

---

### 🔄 Em Andamento

#### Infraestrutura
- Deploy da aplicação
- Mecanismo de backup

---

## Próximo Passo

Fase 3 — Deploy:
- Migrar banco MySQL para nuvem (Railway ou AWS RDS)
- Deploy no Streamlit Community Cloud
- Configurar GitHub Actions para ETL diário

---

## Arquivos Ativos

- `view/main.py` — autenticação implementada
- `view/queries.py` — queries de sono corrigidas, dados sensíveis removidos
- `view/sections/` — páginas com condicionais de dados vazios e labels padronizados
