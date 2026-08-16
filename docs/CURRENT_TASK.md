# Tarefa Atual

## Estado do Desenvolvimento

### ✅ Concluído

#### ETL
- Autenticação com Google OAuth2
- Extração dos dados via Google Sheets API (com retry em HttpError)
- Transformação e padronização dos dados
- Carga no banco MySQL
- Tratamento de erros nas funções `get_*` do `database_loader.py`

#### Banco de Dados
- Modelagem completa do banco `db_oleos`
- População estática via `seed.py` (crianças, observadores, fases, óleos, itens, opções)
- Atributos `turno` e `regular` adicionados à tabela `Crianca`

#### Dashboard — Visão Geral (`general.py`)
- Métricas: total de crianças, responsáveis e professores
- Gráfico de barras: crianças por turno
- Gráfico de barras: registros por fase
- Gráfico de pizza: crianças por fase
- Linha do tempo de registros

#### Dashboard — Análise por Criança (`children.py`)
- Seletor de criança por código
- Resumo: código, idade, turno, regular, professor, responsável
- Gráfico de barras: média por item (linha de base x óleo)
- Gráfico de linha: evolução do sono por fase
- Gráfico de barras: frequência de eventos adversos por fase
- Tabela: comportamento ao ir e voltar da escola por fase (com seletor de fase)

#### Dashboard — Comparações (`comparisons.py`)
- Gráfico de barras: média por turno/regular agrupada por fase
- Gráfico de radar: comparação entre duas crianças por domínio
- Seção de comparação entre óleos essenciais (em andamento)

#### Dashboard — Comparações (`comparisons.py`)
- Comparação entre óleos essenciais (scores por domínio + dados dos pais)
- Comparação linha de base vs intervenção
- Comparação entre ambientes (domiciliar vs escolar)

#### Dashboard — Adesão e Qualidade (`registers.py`)
- Regularidade dos registros por criança
- Gaps no protocolo
- Consistência entre fontes (responsável vs professor)
- Impacto das trocas de óleos entre fases

---

### 🔄 Em Andamento

#### Infraestrutura
- Segurança e controle de acesso (em estudo)
- Deploy da aplicação
- Mecanismo de backup

---

## Próximo Passo

Fase 3 — Segurança e Deploy:
- Estudar e implementar modelo de autenticação
- Refatorar o dashboard com controle de acesso
- Deploy da aplicação
- Mecanismo de backup


---

## Arquivos Ativos

- `view/pages/comparisons.py` — página em desenvolvimento
- `view/queries.py` — novas funções adicionadas para comparação por óleo
