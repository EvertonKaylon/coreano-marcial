<!--
Sync Impact Report
- Version change: none → 1.0.0
- Modified/Added principles: Template placeholders → Domain Supremacy; Mandatory Spec-Driven Development; Security by Default; Explicit Architecture Boundaries; Architectural Decision Logging; Performance as Constraint; Design Token Authority; Documentation Synchronization Rule; Code Quality Enforcement
- Added sections: Constraints & Development Workflow
- Removed sections: none
- Templates updated: .specify/templates/plan-template.md ✅, .specify/templates/spec-template.md ✅, .specify/templates/tasks-template.md ✅
- Follow-up TODOs: verify command templates and create a decisions file when first architectural decision is made
-->

# Coreano Marcial Constitution

## Core Principles

### 1. Domain Supremacy
O domínio do projeto é "ensino de coreano marcial" com progressão estruturada e gamificação. TODA nova feature ou alteração de escopo MUST:

- TER alinhamento explícito com um requisito em `docs/PRD.md` (citar seção ou ID do requisito);
- REFERENCIAR a seção específica do PRD correspondente na `spec` da feature;
- NÃO introduzir complexidade tecnológica que não agregue valor pedagógico direto;

Se não houver alinhamento claro com o PRD, a feature é REJEITADA. Tecnologia existe para servir o domínio, NUNCA o contrário.

### 2. Mandatory Spec-Driven Development
NENHUMA feature pode ser implementada sem:

- Uma especificação formal registrada em `specs/[feature]/spec.md` ou como atualização em `docs/SPEC.md`;
- Critérios de aceite explícitos e mensuráveis;
- Tarefas derivadas da spec (em `specs/[feature]/tasks.md`);
- Referência ao requisito correspondente em `docs/PRD.md`.

Implementação direta sem spec é PROIBIDA. Código é consequência da especificação, nunca o ponto de partida.

### 3. Security by Default
O sistema assume um ambiente hostil. TODA nova funcionalidade MUST:

- Ser avaliada contra os vetores em `docs/threats_v_0.md` (adicionar entradas novas se necessário);
- NÃO confiar em dados do cliente;
- Validar dados no servidor;
- Utilizar proteções nativas do Django (CSRF, autenticação, autorização, validações de formulário/modelo).

É proibido expor lógica sensível no frontend, confiar exclusivamente em validação client-side ou ignorar vetores básicos de abuso. Mudanças que afetam autenticação/autorização/exposição de dados MUST atualizar `docs/threats_v_0.md`.

### 4. Explicit Architecture Boundaries
Arquitetura obrigatória (camadas):

- Domínio (regras de negócio);
- Serviços (orquestração e coordenação);
- Camada HTTP (views/controllers);
- Templates (apresentação).

REGRAS INEGOCIÁVEIS:

- Templates NÃO podem conter lógica de negócio;
- Views NÃO podem conter regras complexas de domínio (devem orquestrar);
- Serviços NÃO dependem de templates;
- Modelos NÃO devem concentrar regras que deveriam estar no domínio.

Desvios devem ser documentados em `docs/decisions_v_X.md`. Código que viole separação de responsabilidades MUST ser refatorado antes do merge.

### 5. Architectural Decision Logging
Toda decisão estrutural relevante MUST:

- Ser registrada em `docs/decisions_v_X.md` (criar novo arquivo versionado por decisão);
- Explicar contexto, decisão e consequências;
- Referenciar a spec associada.

Decisões não documentadas são consideradas inexistentes para fins de auditoria e revisão.

### 6. Performance as Constraint
O projeto assume hardware modesto como baseline. TODA feature MUST:

- Evitar N+1 queries (usar `select_related`/`prefetch_related` quando aplicável);
- NÃO executar processamento pesado em request síncrono sem justificativa;
- Avaliar o impacto de queries em modelos centrais antes de merge;

Qualquer feature que degrade perceptivelmente o tempo de resposta MUST ser revisada e justificada em `plan.md`.

### 7. Design Token Authority
`design_tokens.json` é a única fonte oficial de valores visuais. É proibido:

- Hardcode de cores, espaçamentos críticos ou valores visuais fora do sistema de tokens.

Mudanças visuais MUST:

- Atualizar `design_tokens.json`;
- Regenerar o CSS derivado (onde aplicável);
- Garantir consistência global; interfaces inconsistentes são defeitos estruturais.

### 8. Documentation Synchronization Rule
Os seguintes arquivos são artefatos vivos e MUST ser atualizados quando impactados:

- `docs/PRD.md`;
- `docs/SPEC.md`;
- `docs/threats_v_0.md`;
- `docs/decisions_v_X.md`;
- `docs/code_review_report.md`.

Mudança relevante sem atualização documental correspondente é considerada incompleta. Documentação é parte da entrega.

### 9. Code Quality Enforcement
Relatórios de revisão em `docs/code_review_report.md` MUST ser tratados como dívida ativa. Código que:

- Viole arquitetura;
- Introduza acoplamento indevido;
- Ignore ameaças conhecidas;
- Contradiga a spec;

MUST ser corrigido antes de progresso adicional. Novo código NÃO deve ampliar problemas existentes.

## Constraints & Development Workflow
- Todas as features devem incluir checklist de conformidade com a constituição na PR (`Constitution Compliance`);
- PRs que afetam segurança, autenticação, performance, ou visuais MUST incluir uma seção `Constitution Impact` e atualizar os artefatos mencionados acima.

## Development Workflow & Quality Gates
- Gate obrigatório antes de Phase 0 (Pesquisa): `Constitution Check` (ver lista no `plan.md`);
- Gate obrigatório antes de merge: Spec formal, testes de aceitação, revisão de segurança, e aprovação de maintainers;
- Mudanças arquiteturais significativas MUST incluir arquivo em `docs/decisions_v_X.md` e passar por revisão adicional.

## Governance
- Emendas à constituição MUST ser propostas via PR que inclua:
  - A versão atualizada de `.specify/memory/constitution.md`;
  - Um `Sync Impact Report` (como comentário HTML no topo do arquivo) listando mudanças e arquivos afetados;
  - Proposta de `CONSTITUTION_VERSION` e motivo do bump (MAJOR/MINOR/PATCH) conforme regras abaixo.

- Versionamento da constituição (semântico):
  - MAJOR: mudanças incompatíveis (remoção/reescrita de princípios);
  - MINOR: adição de princípios ou novas seções com requisitos novos;
  - PATCH: esclarecimentos, correções de texto e pequenas reformulações que NÃO mudem a intenção.

- Aprovação: PRs de emenda MUST ter aprovação de pelo menos um maintainer listado no repositório e passar CI/linters. Quando aplicável, as emendas que afetam áreas sensíveis (segurança, autenticação, privacidade) MUST ter revisão adicional por um maintainer com responsabilidade nessa área.

**Version**: 1.0.0 | **Ratified**: 2026-02-02 | **Last Amended**: 2026-02-02
