# Inventário de Tasks, Issues e PRs existentes

**Data:** 2026-02-06
**Objetivo:** consolidar onde estão as tarefas formais do projeto e quais PRs/issues já aparecem no histórico.

## 1) Tasks formais no repositório

Fonte principal: `specs/001-add-prd/tasks.md`.

- O arquivo lista as tasks **T001 a T013** para o ciclo `001-add-prd`.
- Todas ainda estão marcadas como pendentes (`[ ]`) no arquivo, inclusive itens que já parecem ter sido implementados via PRs/commits.
- Há tasks marcadas como **DEPRECATED** (`T007`, `T008`) e redirecionadas para `T012/T013`.

### Resumo por fase

- **Fase 1 (Setup & Drafting):** T001, T002, T003
- **Fase 2 (Review & Governance):** T004, T005, T006, T011
- **Fase 3 (CI & Automation):** T012, T013 (+ T007/T008 deprecated)
- **Fase 4 (Follow-ups):** T009, T010

## 2) Issues/épicos já referenciados no projeto

Fonte: `specs/001-add-prd/checklists/track_issues.md`.

- Epic requisitos gerais: issue **#5**
- Epic requisitos PRD: issue **#6**
- Gap CHK012: issue **#2**
- Gap CHK014: issue **#3**
- Gap CHK016: issue **#4**

## 3) PRs já visíveis no histórico Git local

Com base no `git log` local, aparecem merges de PR:

- **PR #7** — `chore/chk012-zero-state`
- **PR #8** — `chore/chk014-fallback`
- **PR #9** — `chore/chk016-a11y`
- **PR #11** — `chore/add-codeowners`

Também existem commits recentes no branch de trabalho (`work`) ainda não refletidos como merge no histórico principal deste clone.

## 4) Governança de PR documentada

O processo obrigatório para PRs está documentado no `README.md` em "Pull Request & Governance", incluindo:

- `Constitution Compliance`
- `Sync Impact Report`
- `Designated Reviewer`
- Regras de revisão de segurança quando aplicável

## 5) Próxima ação recomendada

Para manter rastreabilidade correta entre execução e planejamento:

1. Atualizar `specs/001-add-prd/tasks.md` marcando como concluídas as tasks já entregues.
2. Referenciar no arquivo de tasks o PR/commit que concluiu cada item.
3. Fechar issues já resolvidas nos épicos #5/#6 e manter apenas gaps realmente abertos.
