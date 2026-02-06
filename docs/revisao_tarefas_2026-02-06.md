# Revisão rápida da base de código (2026-02-06)

## Objetivo
Listar problemas encontrados e propor 4 tarefas priorizadas: correção de digitação, bug, discrepância de comentário/documentação e melhoria de teste.

## Tarefa 1 — Corrigir erro de digitação/termo na documentação

**Problema encontrado**
O README mistura documentação em português com o rótulo em inglês `Database` na seção de stack, o que destoa do restante da documentação e pode confundir leitores menos técnicos.

**Evidência**
- `README.md` usa `Database: PostgreSQL` enquanto o restante está em português.

**Tarefa sugerida**
Padronizar o item para `Banco de dados: PostgreSQL` (ou traduzir toda a seção para inglês, se essa for a convenção desejada).

**Critério de aceite**
- Seção de stack com terminologia consistente em um único idioma.

---

## Tarefa 2 — Corrigir bug na dashboard de progresso

**Problema encontrado**
A view calcula `completed_lessons` e `mastered_vocab`, mas o template exibe os campos persistidos `user_progress.total_lessons_completed` e `user_progress.total_vocabulary_mastered`, que podem ficar desatualizados e mostrar números incorretos para o usuário.

**Evidência**
- Cálculo dinâmico na view: `apps/progress/views.py`
- Exibição de campos agregados persistidos no template: `templates/progress/dashboard.html`

**Tarefa sugerida**
Escolher uma fonte única da verdade:
1. Ou exibir no template os contadores dinâmicos (`completed_lessons`, `mastered_vocab`);
2. Ou atualizar sempre os campos `total_*` via signals/serviço e parar de calcular no request.

**Critério de aceite**
- Os números mostrados em "Status Atual" batem com os critérios de avanço exibidos na mesma página.

---

## Tarefa 3 — Ajustar ambiguidade de documentação (PRD/SPEC/README)

**Problema encontrado**
Após leitura de PRD e SPEC completos, a discrepância "HTMX na Fase 0" **não é um conflito real de escopo**: tanto README quanto SPEC detalham que Fase 0 usa renderização full-page sem HTMX, e HTMX entra na Fase 1.

O ponto que permanece é uma **ambiguidade de redação** na "Visão Geral" da SPEC, que cita a arquitetura alvo com Django + HTMX antes de detalhar o faseamento.

**Evidência**
- `docs/PRD.md` define stack-alvo com HTMX/PWA, mas o roadmap por fases separa entregas.
- `docs/SPEC.md` (seções de faseamento e escopo) diz explicitamente que Fase 0 não inclui HTMX.
- `README.md` também diz que Fase 0 é sem HTMX.

**Tarefa sugerida**
Ajustar apenas a redação introdutória da SPEC para reduzir ambiguidade (ex.: indicar explicitamente que Django + HTMX é visão de produto/fases futuras, não requisito imediato da Fase 0).

**Critério de aceite**
- Leitor novo entende, sem contradição aparente, que HTMX é parte da visão do produto e da Fase 1, não da implementação da Fase 0.

---

## Tarefa 4 — Melhorar cobertura de testes para validação de áudio

**Problema encontrado**
A validação de `AudioFile.clean()` cobre alguns casos, mas não protege explicitamente combinações inconsistentes de `audio_type` com a FK preenchida (ex.: `audio_type='lesson'` com apenas `vocabulary` definido).

**Evidência**
- Lógica atual em `apps/audio/models.py` valida ausência em alguns cenários, mas não afirma a correspondência tipo↔relacionamento em ambos os sentidos.

**Tarefa sugerida**
Adicionar testes de modelo para matriz completa de casos:
- `lesson` válido;
- `vocabulary` válido;
- ambos preenchidos (inválido);
- nenhum preenchido (inválido);
- tipo e FK inconsistente (inválido nos dois sentidos).

**Critério de aceite**
- Testes falham com a implementação atual para casos inconsistentes e passam após ajuste da validação.
