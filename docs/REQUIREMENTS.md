# Requisitos do Sistema

## 1. Requisitos Funcionais

Os requisitos funcionais descrevem as funcionalidades e capacidades que o
sistema deverá oferecer para atender às necessidades do estudo científico.

### RF01 — Avaliação do efeito da aromaterapia

O sistema deve permitir a análise da variação dos comportamentos observados
nas crianças participantes durante o período de intervenção com aromaterapia.

### RF02 — Comparação entre óleos essenciais

O sistema deve permitir comparar os resultados comportamentais obtidos durante
a utilização de diferentes óleos essenciais do protocolo experimental.

### RF03 — Análise da evolução comportamental

O sistema deve permitir visualizar e analisar a evolução dos comportamentos
observados ao longo do tempo, considerando a sequência das fases do protocolo
experimental.

### RF04 — Comparação entre ambientes

O sistema deve permitir comparar os registros comportamentais realizados em
diferentes ambientes, incluindo, no mínimo:

- ambiente domiciliar;
- ambiente escolar.

### RF05 — Análise de respostas individuais

O sistema deve permitir identificar e analisar diferenças na resposta à
intervenção entre as crianças participantes, considerando os dados individuais
de cada participante.

### RF06 — Avaliação da adesão ao protocolo

O sistema deve permitir avaliar a adesão ao protocolo de aplicação dos óleos
essenciais por meio da análise da regularidade e completude dos registros
realizados.

### RF07 — Registro de eventos adversos

O sistema deve permitir registrar possíveis eventos adversos observados durante
o período de intervenção.

### RF08 — Monitoramento de eventos adversos

O sistema deve permitir consultar e analisar os eventos adversos registrados,
possibilitando sua associação ao participante, período, fase e óleo essencial
utilizado.

### RF09 — Comparação com a linha de base

O sistema deve permitir comparar os dados comportamentais obtidos durante as
fases de intervenção com os dados registrados durante o período de linha de
base (pré-intervenção).

### RF10 — Análise das trocas de óleo

O sistema deve permitir analisar alterações nos comportamentos observados após
a troca do óleo essencial entre diferentes fases do protocolo experimental.

### RF11 — Comparação entre fontes de observação

O sistema deve permitir comparar as avaliações realizadas por diferentes fontes
de observação, incluindo:

- responsáveis, com avaliações diárias;
- professores, com avaliações semanais.

### RF12 — Análise da consistência entre avaliadores

O sistema deve permitir analisar o grau de concordância ou diferença entre as
avaliações realizadas por responsáveis e professores para um mesmo participante
e período de observação.

### RF13 — Comparação entre turnos

O sistema deve permitir comparar os dados comportamentais de crianças
pertencentes a diferentes turnos escolares ou períodos de atendimento.

### RF14 — Filtragem dos dados

O sistema deve permitir filtrar os dados das análises considerando, quando
aplicável:

- participante;
- óleo essencial;
- fase do protocolo;
- período;
- ambiente;
- turno;
- fonte de observação;
- comportamento avaliado.

### RF15 — Visualização dos resultados

O sistema deve permitir visualizar os resultados das análises por meio de
tabelas e representações gráficas adequadas aos dados coletados.

### RF16 — Consulta dos dados individuais

O sistema deve permitir consultar o histórico de avaliações de cada
participante ao longo das diferentes fases do estudo.

### RF17 — Identificação das fases do protocolo

O sistema deve associar cada registro à respectiva fase do protocolo
experimental, permitindo diferenciar, no mínimo:

- linha de base;
- fases de intervenção;
- períodos de troca de óleo, quando aplicável.

### RF18 — Associação dos registros ao contexto da avaliação

Cada avaliação registrada deve permitir identificar, quando aplicável:

- participante;
- data;
- fase do protocolo;
- óleo essencial utilizado;
- ambiente;
- turno;
- fonte de observação;
- comportamentos avaliados.

---

## 2. Requisitos Não Funcionais

Os requisitos não funcionais definem características de qualidade, segurança,
confiabilidade e manutenção esperadas para o sistema.

### RNF01 — Integridade dos dados

O sistema deve garantir a integridade dos dados registrados, evitando
inconsistências entre participantes, avaliações, fases do protocolo e óleos
essenciais.

### RNF02 — Persistência dos dados

Os dados registrados devem permanecer armazenados após o encerramento da
aplicação.

### RNF03 — Confiabilidade

O sistema deve minimizar a ocorrência de perda ou alteração indevida dos
dados coletados durante o estudo.

### RNF04 — Segurança

O sistema deve impedir que usuários não autorizados tenham acesso aos dados
do estudo.

### RNF05 — Controle de acesso

O sistema deve permitir controlar o acesso às funcionalidades de acordo com
o perfil do usuário, quando houver diferentes tipos de usuários.

### RNF06 — Privacidade

O sistema deve tratar os dados dos participantes de forma a reduzir a
exposição de informações que possam identificar diretamente as crianças
participantes.

### RNF07 — Usabilidade

As telas de registro e consulta devem apresentar uma interface simples e
intuitiva, permitindo que os usuários realizem suas atividades sem
necessidade de conhecimento técnico.

### RNF08 — Desempenho

As operações de consulta e visualização dos dados devem apresentar tempo de
resposta adequado para o volume de dados esperado pelo estudo.

### RNF09 — Disponibilidade

O sistema deve permanecer disponível durante os períodos em que os
pesquisadores e demais usuários necessitarem realizar registros e consultas.

### RNF10 — Manutenibilidade

O código deve ser organizado de forma modular, permitindo a manutenção,
correção e evolução das funcionalidades sem impactos desnecessários em
outras partes do sistema.

### RNF11 — Escalabilidade

A estrutura do sistema deve permitir o aumento do número de participantes,
avaliações e fases do estudo sem necessidade de alterações estruturais
significativas.

### RNF12 — Rastreabilidade

O sistema deve manter informações suficientes para identificar a origem e o
contexto dos registros utilizados nas análises.

### RNF13 — Compatibilidade

A aplicação web deve funcionar nos principais navegadores modernos utilizados
pelos pesquisadores e demais usuários do sistema.

### RNF14 — Consistência das análises

Os resultados apresentados pelo sistema devem ser calculados a partir dos
dados armazenados de forma consistente e reproduzível.

### RNF15 — Backup

O sistema deve possuir mecanismo de cópia de segurança dos dados, permitindo
a recuperação das informações em caso de falha ou perda de dados.

---

## 3. Resumo dos Requisitos

### Requisitos Funcionais

| ID | Requisito |
|---|---|
| RF01 | Avaliação do efeito da aromaterapia |
| RF02 | Comparação entre óleos essenciais |
| RF03 | Análise da evolução comportamental |
| RF04 | Comparação entre ambientes |
| RF05 | Análise de respostas individuais |
| RF06 | Avaliação da adesão ao protocolo |
| RF07 | Registro de eventos adversos |
| RF08 | Monitoramento de eventos adversos |
| RF09 | Comparação com a linha de base |
| RF10 | Análise das trocas de óleo |
| RF11 | Comparação entre fontes de observação |
| RF12 | Análise da consistência entre avaliadores |
| RF13 | Comparação entre turnos |
| RF14 | Filtragem dos dados |
| RF15 | Visualização dos resultados |
| RF16 | Consulta dos dados individuais |
| RF17 | Identificação das fases do protocolo |
| RF18 | Associação dos registros ao contexto |

### Requisitos Não Funcionais

| ID | Requisito |
|---|---|
| RNF01 | Integridade dos dados |
| RNF02 | Persistência dos dados |
| RNF03 | Confiabilidade |
| RNF04 | Segurança |
| RNF05 | Controle de acesso |
| RNF06 | Privacidade |
| RNF07 | Usabilidade |
| RNF08 | Desempenho |
| RNF09 | Disponibilidade |
| RNF10 | Manutenibilidade |
| RNF11 | Escalabilidade |
| RNF12 | Rastreabilidade |
| RNF13 | Compatibilidade |
| RNF14 | Consistência das análises |
| RNF15 | Backup |