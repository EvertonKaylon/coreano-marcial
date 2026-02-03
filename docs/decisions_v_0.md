# DECISIONS v0.1 — Coreano Marcial

Este documento registra as **decisões arquiteturais e pedagógicas fundamentais** do projeto Coreano Marcial.

Cada decisão aqui documentada existe para **reduzir ambiguidade futura**, evitar retrabalho e manter coerência com a SPEC v0.1.

Nenhuma decisão registrada aqui deve ser alterada sem uma nova entrada numerada.

---

## D001 — Aplicação Web em vez de App Nativo

**Decisão:** Desenvolver o sistema como aplicação Web (SPA + PWA), e não como app nativo Android/iOS.

**Motivo:**
- Um único código-base atende mobile e desktop
- PWA permite instalação, offline e experiência próxima de app nativo
- Reduz custo, tempo e complexidade operacional
- Maior controle pedagógico sem depender de lojas

**Consequência:**
- A performance deve ser cuidadosamente otimizada
- Algumas APIs nativas podem não estar disponíveis em todos os dispositivos

---

## D002 — SPA (Single Page Application)

**Decisão:** A aplicação será uma SPA.

**Motivo:**
- Navegação fluida sem recarregamento
- Manutenção de estado (áudio, contexto, painéis)
- Imersão contínua no estudo

**Consequência:**
- Estrutura de App Shell obrigatória
- Gerenciamento consciente de cache e estado

---

## D003 — SPA sem Frameworks Pesados (React/Vue/Angular)

**Decisão:** Não utilizar frameworks frontend pesados.

**Motivo:**
- Complexidade desnecessária para o escopo
- Curva de aprendizado maior
- Lógica pedagógica já reside no backend
- HTMX oferece interatividade suficiente

**Consequência:**
- Mais responsabilidade no backend
- UI orientada a HTML server-driven

---

## D004 — Django como Backend Principal

**Decisão:** Utilizar Django como framework backend.

**Motivo:**
- Robustez e maturidade
- ORM poderoso para dados pedagógicos complexos
- Integração natural com HTMX
- Familiaridade com o ecossistema Python

**Consequência:**
- Estrutura MVC rigorosa
- Separação clara entre regras de negócio e apresentação

---

## D005 — HTMX como Motor de Interatividade

**Decisão:** Usar HTMX para interações dinâmicas.

**Motivo:**
- Permite comportamento de SPA sem JS complexo
- HTML continua sendo a fonte da verdade
- Facilita manutenção a longo prazo

**Consequência:**
- Dependência de fragmentos HTML bem definidos
- Arquitetura orientada a componentes server-side

---

## D006 — Mobile-First Real

**Decisão:** Projetar a UI inicialmente para mobile.

**Motivo:**
- Principal contexto de uso (ônibus, casa, treino)
- Força simplicidade e clareza
- Desktop será uma expansão natural

**Consequência:**
- Interfaces precisam funcionar bem com uma mão
- Elementos grandes e hierarquia visual clara

---

## D007 — Zero Romanização Visível

**Decisão:** Proibir romanização visível ao usuário.

**Motivo:**
- Romanização cria vícios fonéticos
- Interfere na fluência real
- Vai contra os princípios científicos do Hangeul

**Consequência:**
- Necessidade de fonética visual e áudio de alta qualidade
- Curva inicial mais exigente para iniciantes

---

## D008 — Fonética Científica Interna (IPA)

**Decisão:** Armazenar fonética usando IPA internamente.

**Motivo:**
- Permite análise precisa de pronúncia
- Independe de romanizações inconsistentes
- Base para correção fonética futura

**Consequência:**
- Usuário não vê IPA diretamente
- Backend precisa lidar com dados linguísticos

---

## D009 — Conteúdo Hierárquico Marcial

**Decisão:** Filtrar conteúdo por nível marcial.

**Motivo:**
- Evita sobrecarga cognitiva
- Respeita a progressão tradicional
- Aumenta autoridade pedagógica

**Consequência:**
- Sistema de permissões mais elaborado
- Conteúdo precisa ser cuidadosamente categorizado

---

## D010 — Conteúdo WSHF como Referência Inicial

**Decisão:** Usar a estrutura da World Sport Hapkido Federation como base inicial.

**Motivo:**
- Currículo organizado e tradicional
- Autoridade marcial reconhecida
- Facilita expansão futura

**Consequência:**
- Conteúdo precisa ser fiel à fonte
- Alterações exigem critério histórico e técnico

---

## D011 — Sem Gamificação Competitiva Inicial

**Decisão:** Não implementar rankings, pontuações públicas ou competição entre usuários na v0.1.

**Motivo:**
- Foco em aprendizado profundo, não em recompensa superficial
- Evita distorção do propósito marcial

**Consequência:**
- Engajamento baseado em progresso pessoal
- Gamificação pode ser avaliada futuramente

---

## D012 — Evolução Controlada

**Decisão:** O sistema evoluirá por versões pequenas e controladas.

**Motivo:**
- Reduz risco arquitetural
- Facilita validação pedagógica
- Mantém o projeto sustentável

**Consequência:**
- Funcionalidades avançadas entram apenas após base sólida

---

**Este documento é complementar à SPEC v0.1.**

Quando houver conflito, a SPEC tem precedência.

