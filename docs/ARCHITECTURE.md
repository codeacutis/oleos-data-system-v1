# Arquitetura do Sistema

## Visão Geral

O sistema segue o padrão ETL (Extract, Transform, Load) para coleta e processamento dos dados, com uma camada de visualização separada desenvolvida em Streamlit.

```
Google Forms / Google Sheets
            │
            ▼
       Extract (extract/sheets_extractor.py)
            │
            ▼
      Transform (transform/transform_data.py)
            │
            ▼
         MySQL (db_oleos)
            │
            ▼
 Dashboard Streamlit (view/)
```

---

## Estrutura de Pastas

```
etl-oleos/
├── auth/
│   ├── google_auth.py        # Autenticação OAuth2 com Google
│   ├── client_secret.json    # Credenciais OAuth (não versionado)
│   └── token.json            # Token de acesso (não versionado)
│
├── extract/
│   └── sheets_extractor.py   # Extração dos dados via Google Sheets API
│
├── transform/
│   └── transform_data.py     # Transformação e padronização dos dados
│
├── load/
│   ├── db_connection.py      # Conexão com o banco MySQL
│   ├── database_loader.py    # Funções de carga no banco
│   └── seed.py               # População estática do banco (IDs hardcoded)
│
├── view/
│   ├── main.py               # Entry point do Streamlit (st.navigation)
│   ├── config.py             # Configuração do sys.path
│   ├── db.py                 # Conexão cacheada e execução de queries
│   ├── queries.py            # Queries SQL estáticas e funções dinâmicas
│   └── pages/
│       ├── general.py        # Página: Visão Geral
│       ├── children.py       # Página: Análise por Criança
│       ├── comparisons.py    # Página: Comparações
│       └── registers.py      # Página: Adesão e Qualidade
│
├── app.py                    # Execução do processo ETL completo
├── config.yaml               # Configurações dos formulários (não versionado)
├── config.yaml.example       # Template do config.yaml
└── docs/                     # Documentação do projeto
```

---

## Módulos

### auth
Responsável pela autenticação com a API do Google via OAuth2. Gera e renova o `token.json` automaticamente.

### extract
Consome a Google Sheets API para extrair as respostas dos formulários. Utiliza `@retry` para lidar com falhas de rede (`HttpError`).

### transform
Recebe os dados brutos extraídos e os transforma para o formato esperado pelo banco de dados. Separa registros de responsáveis e professores.

### load
Contém as funções de persistência no banco MySQL. O `seed.py` popula os dados estáticos (crianças, observadores, fases, óleos, itens de escala). O `database_loader.py` contém as funções `get_*` e `load_*` para inserção dos registros.

### view
Camada de visualização desenvolvida em Streamlit. Organizada em páginas independentes dentro de `pages/`. O `db.py` utiliza `@st.cache_resource` para manter a conexão com o banco entre reruns.

---

## Banco de Dados

Banco: `db_oleos` — MySQL

### Tabelas de Referência Estática
- `Oleo` — óleos essenciais utilizados no protocolo
- `Fase_Estudo` — fases do protocolo com datas e óleo associado
- `Formulario` — formulários por fase e tipo de observador
- `Dominio_Escala` — domínios de comportamento avaliados
- `Item_Escala` — itens dos formulários com tipo de resposta
- `Opcao_Categorica` — opções de resposta categórica
- `Opcao_Checkbox` — opções de resposta checkbox

### Tabelas de Participantes
- `Crianca` — participantes do estudo (código, nascimento, sexo, turno, regular)
- `Observador` — responsáveis e professores vinculados às crianças
- `Observador_Crianca` — relação entre observador, criança e ambiente

### Tabelas de Registros
- `Registro` — cada formulário respondido (data, criança, observador, fase, formulário)
- `Resposta` — respostas numéricas, categóricas e de texto
- `Resposta_Checkbox` — respostas do tipo checkbox

---

## Fluxo de Execução

### ETL
```bash
python app.py
```
1. Autentica com Google
2. Extrai respostas de todos os formulários configurados no `config.yaml`
3. Transforma os dados
4. Carrega no banco MySQL

### Dashboard
```bash
streamlit run view/main.py
```
1. Conecta ao banco MySQL
2. Executa queries sob demanda
3. Renderiza visualizações interativas
