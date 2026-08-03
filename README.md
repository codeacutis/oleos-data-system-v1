# Óleos Data System

## Sobre o projeto

O **Óleos Data System** é um sistema desenvolvido para apoiar uma pesquisa científica sobre os efeitos da aromaterapia em crianças com Transtorno do Espectro Autista (TEA).

O projeto automatiza todo o fluxo de coleta, processamento e visualização dos dados obtidos por meio de formulários eletrônicos, permitindo que pesquisadores acompanhem os resultados da pesquisa de maneira centralizada.

Além da organização dos dados, o sistema disponibiliza um painel interativo para consulta de indicadores e análises, reduzindo o trabalho manual de tratamento das informações.

---

## Objetivos

* Automatizar a coleta de respostas dos formulários da pesquisa.
* Padronizar e transformar os dados recebidos.
* Armazenar as informações em um banco de dados relacional.
* Disponibilizar dashboards para acompanhamento dos participantes e dos resultados da pesquisa.
* Facilitar a análise dos dados pelos pesquisadores.

---

## Arquitetura

O projeto foi organizado em módulos independentes seguindo o fluxo de um processo ETL (Extract, Transform and Load).

```text
Google Forms / Google Sheets
            │
            ▼
       Extract
            │
            ▼
      Transform
            │
            ▼
         MySQL
            │
            ▼
 Dashboard Streamlit
```

### Estrutura do projeto

```text
auth/
    Autenticação com Google

extract/
    Extração dos dados dos formulários

transform/
    Tratamento e padronização das informações

load/
    Persistência dos dados no banco MySQL

view/
    Dashboard desenvolvido em Streamlit

app.py
    Execução do processo ETL
```

---

## Tecnologias utilizadas

* Python
* Streamlit
* MySQL
* Google Sheets API
* Google Forms
* Plotly
* Pandas
* YAML

---

## Funcionalidades implementadas

### ETL

* Extração automática dos dados dos formulários
* Transformação dos dados coletados
* Separação dos registros de responsáveis e professores
* Tratamento das respostas
* Persistência no banco de dados

### Dashboard

* Visão geral da pesquisa
* Total de crianças cadastradas
* Total de responsáveis
* Total de professores
* Distribuição de participantes por turno
* Quantidade de questionários respondidos por fase
* Distribuição das crianças durante o protocolo
* Linha do tempo dos registros

---

## Em desenvolvimento

O projeto continua em evolução. Entre as funcionalidades previstas estão:

* Novas análises estatísticas
* Comparações entre fases do protocolo
* Melhorias na interface do dashboard
* Exportação de relatórios
* Novos indicadores para os pesquisadores
* Melhorias na documentação
* Deploy da aplicação

---

## Como executar

### 1. Clone o projeto

```bash
git clone https://github.com/codeacutis/oleos-data-system-v1.git
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure as credenciais

Crie um arquivo `config.yaml` utilizando como base o arquivo:

```text
config.yaml.example
```

Configure:

* credenciais da Google API;
* acesso ao banco de dados;
* demais parâmetros da aplicação.

### 4. Execute o processo ETL

```bash
python app.py
```

### 5. Execute o dashboard

```bash
streamlit run view/main.py
```

---

## Status

🚧 Projeto em desenvolvimento.

Este projeto está sendo desenvolvido como parte de uma pesquisa científica e continua recebendo novas funcionalidades e melhorias conforme o avanço do estudo.

---

## Aprendizados

Durante o desenvolvimento deste projeto foram aplicados conceitos de:

* Engenharia de Dados (ETL)
* Integração com APIs Google
* Manipulação e transformação de dados
* Banco de dados relacional
* Visualização de dados
* Desenvolvimento de dashboards
* Organização em camadas
* Automação de processos de coleta de dados

---

## Licença

Projeto desenvolvido para fins acadêmicos e de pesquisa.
