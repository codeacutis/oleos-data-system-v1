# Domínio do Problema

## Contexto

Este sistema apoia uma pesquisa científica que investiga os efeitos da **aromaterapia** no comportamento de crianças com **Transtorno do Espectro Autista (TEA)**.

O estudo é conduzido por pesquisadores e envolve crianças participantes, seus responsáveis e professores. Os dados são coletados por meio de formulários eletrônicos (Google Forms) respondidos periodicamente ao longo de um protocolo experimental estruturado em fases.

---

## Glossário

### TEA — Transtorno do Espectro Autista
Condição do neurodesenvolvimento caracterizada por variações na comunicação social, comportamento e processamento sensorial. As crianças participantes do estudo possuem diagnóstico confirmado de TEA.

### Aromaterapia
Prática terapêutica que utiliza óleos essenciais com o objetivo de promover bem-estar físico e emocional. Neste estudo, os óleos são aplicados nas crianças seguindo um protocolo experimental controlado.

### Protocolo Experimental
Conjunto de regras e etapas que definem como o estudo é conduzido. O protocolo define quais óleos são utilizados, em qual ordem, por quanto tempo e como os dados devem ser coletados.

### Fase do Estudo
Período delimitado do protocolo experimental. Cada fase possui:
- Nome identificador
- Ordem de execução
- Data de início e data de fim
- Óleo essencial associado (exceto a linha de base)

As fases do estudo são:
1. **Linha de Base** — período pré-intervenção, sem aplicação de óleo
2. **Lavanda** — fase com aplicação de óleo de lavanda
3. **Mandarina** — fase com aplicação de óleo de mandarina
4. **Patchouli** — fase com aplicação de óleo de patchouli
5. **Ylang Ylang** — fase com aplicação de óleo de ylang ylang

### Linha de Base
Período inicial do estudo, anterior à intervenção com óleos essenciais. Serve como referência para comparação com os dados coletados durante as fases de intervenção.

### Óleo Essencial
Substância utilizada na intervenção. Cada fase de intervenção utiliza um óleo diferente, permitindo comparar a eficácia entre eles.

### Criança Participante
Criança com diagnóstico de TEA que participa do estudo. Cada criança possui:
- Código identificador (ex: CR001)
- Data de nascimento
- Sexo
- Diagnóstico
- Turno escolar (`MANHÃ`, `TARDE`, `INTEGRAL`)
- Turno regular (`MANHÃ`, `TARDE`) — turno efetivo de ensino, relevante para crianças no integral

### Turno e Regular
- **Turno**: período em que a criança permanece na escola (`MANHÃ`, `TARDE`, `INTEGRAL`)
- **Regular**: período do ensino regular da criança (`MANHÃ`, `TARDE`)
- Crianças com turno `MANHÃ` ou `TARDE` têm `regular` com o mesmo valor
- Crianças com turno `INTEGRAL` podem ter `regular` como `MANHÃ` ou `TARDE`

### Observador
Pessoa responsável por preencher os formulários de avaliação. Existem dois tipos:
- **Responsável** (`RESPONSAVEL`): familiar ou responsável legal da criança, realiza avaliações **diárias** no ambiente domiciliar
- **Professor** (`PROFESSOR`): educador da criança, realiza avaliações **semanais** no ambiente escolar

### Ambiente
Contexto em que a observação é realizada:
- **Domiciliar**: ambiente familiar, avaliado pelos responsáveis
- **Escolar**: ambiente da escola, avaliado pelos professores

### Formulário
Instrumento de coleta de dados. Cada formulário está associado a uma fase e a um tipo de observador (`PAIS` ou `PROFESSOR`). Os formulários são disponibilizados via Google Forms e as respostas são armazenadas em Google Sheets.

### Item de Escala
Pergunta individual de um formulário. Cada item possui:
- Descrição (texto da pergunta)
- Tipo de resposta
- Tipo de observador (quem responde)
- Domínio ao qual pertence (apenas para itens de professores)

### Tipos de Resposta
- **ESCALA_0_4**: escala numérica de 0 a 4 (0 = nunca, 4 = sempre). Utilizada nos formulários de professores para avaliar comportamentos observáveis em sala de aula.
- **SIM_NAO**: resposta binária. Utilizada nos formulários de responsáveis para registrar eventos adversos.
- **CATEGORICO**: seleção de uma opção entre várias. Utilizada para registrar comportamento e estado emocional.
- **SONO**: registro do período de sono da criança.
- **CHECKBOX**: seleção múltipla de opções.
- **TEXTO_LIVRE**: campo aberto para observações.

### Domínio de Escala
Agrupamento temático dos itens de avaliação dos professores:
- **Interação Social**: comportamentos relacionados à interação com colegas e participação em atividades coletivas
- **Ansiedade e Estresse**: comportamentos relacionados à agitação, impulsividade, ansiedade e desatenção
- **Aprendizado**: comportamentos relacionados ao engajamento e desempenho nas atividades escolares
- **Verificação Semanal**: checklist semanal de eventos observados
- **Observações**: campo livre para anotações do professor

### Registro
Instância de um formulário respondido. Cada registro representa uma avaliação realizada por um observador para uma criança em uma data específica, dentro de uma fase do protocolo.

### Resposta
Valor registrado para um item de escala dentro de um registro. Pode ser numérico, categórico ou textual, dependendo do tipo do item.

### Evento Adverso
Ocorrência indesejada observada durante o período de intervenção, como agitação noturna, sinais de ansiedade ou mudanças de comportamento. Registrado pelos responsáveis via itens `SIM_NAO`.
