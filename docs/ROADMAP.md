# Roadmap

## Versão 1.0 — MVP do Dashboard

### ✅ Fase 1 — Infraestrutura e ETL
- [x] Modelagem do banco de dados
- [x] Autenticação com Google API
- [x] Extração dos dados dos formulários
- [x] Transformação dos dados
- [x] Carga no banco MySQL
- [x] População estática do banco (seed)

### 🔄 Fase 2 — Dashboard de Visualização
- [x] Estrutura de navegação (Streamlit multipage)
- [x] Página: Visão Geral
- [x] Página: Análise por Criança
- [ ] Página: Comparações (em andamento)
- [ ] Página: Adesão dos Pais e Qualidade

### ⬜ Fase 3 — Segurança e Deploy
- [ ] Controle de acesso por perfil de usuário
- [ ] Proteção dos dados dos participantes
- [ ] Deploy da aplicação
- [ ] Mecanismo de backup

---

## Versão 2.0 — Melhorias e Expansão

### Análises Avançadas
- [ ] Exportação de relatórios em PDF
- [ ] Análises estatísticas mais robustas
- [ ] Novos indicadores para os pesquisadores

### Infraestrutura
- [ ] Automação do processo ETL (agendamento)
- [ ] Monitoramento de erros em produção
- [ ] Documentação técnica completa

---

## Páginas do Dashboard

| Página | Pergunta Central | Status |
|---|---|---|
| Visão Geral | Como está o estudo? | ✅ Concluída |
| Análise por Criança | Como esta criança respondeu ao protocolo? | ✅ Concluída |
| Comparações | Quais diferenças aparecem entre óleos, ambientes e grupos? | 🔄 Em andamento |
| Adesão e Qualidade | Os dados coletados são suficientes e consistentes? | ⬜ Pendente |

---

## Requisitos Cobertos por Página

| Requisito | Página |
|---|---|
| RF01 — Avaliação do efeito da aromaterapia | Análise por Criança |
| RF02 — Comparação entre óleos essenciais | Comparações |
| RF03 — Análise da evolução comportamental | Análise por Criança |
| RF04 — Comparação entre ambientes | Análise por Criança / Comparações |
| RF05 — Análise de respostas individuais | Análise por Criança |
| RF06 — Avaliação da adesão ao protocolo | Adesão e Qualidade |
| RF07 — Registro de eventos adversos | Análise por Criança |
| RF08 — Monitoramento de eventos adversos | Análise por Criança / Comparações |
| RF09 — Comparação com a linha de base | Análise por Criança / Comparações |
| RF10 — Análise das trocas de óleo | Comparações |
| RF11 — Comparação entre fontes de observação | Adesão e Qualidade |
| RF12 — Consistência entre avaliadores | Adesão e Qualidade |
| RF13 — Comparação entre turnos | Comparações |
| RF14 — Filtragem dos dados | Todas as páginas |
| RF15 — Visualização dos resultados | Todas as páginas |
| RF16 — Consulta dos dados individuais | Análise por Criança |
| RF17 — Identificação das fases do protocolo | Todas as páginas |
| RF18 — Associação dos registros ao contexto | Análise por Criança |
