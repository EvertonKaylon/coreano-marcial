# THREATS v0.1 — Coreano Marcial

Este documento descreve o **modelo de ameaças inicial** do projeto Coreano Marcial.

Ele não existe para gerar paranoia abstrata, mas para **orientar decisões técnicas reais** desde o primeiro commit.

A pergunta central não é *"se"* o sistema será atacado, mas **como**, **por quem** e **com que impacto**.

---

## Mentalidade Base

- O sistema **sempre será público** (aplicação web)
- Qualquer endpoint será eventualmente observado
- Ataques não começam sofisticados — eles escalam
- Segurança não é feature, é condição de existência

---

## Superfície de Ataque Principal

- Interface web pública
- Endpoints HTMX
- Área administrativa
- Pipeline de deploy
- Dependências de terceiros

---

## Classes de Ameaça Consideradas

### 1. Ameaças de Autenticação e Sessão

**Riscos:**
- Sequestro de sessão
- Fixação de sessão
- Uso indevido de cookies

**Mitigações Iniciais:**
- Cookies HttpOnly e Secure
- Rotação adequada de sessão
- Expiração controlada

---

### 2. Ameaças de Autorização

**Riscos:**
- Acesso indevido a conteúdo restrito
- Elevação de privilégios
- Enumeração de recursos

**Mitigações Iniciais:**
- Verificação explícita de permissões
- Falhas silenciosas para usuários não autorizados
- IDs não previsíveis

---

### 3. Injeções e Manipulação de Dados

**Riscos:**
- SQL Injection
- Injeção lógica
- Manipulação de parâmetros HTMX

**Mitigações Iniciais:**
- ORM estrito
- Validação de entrada em todos os níveis
- Nunca confiar em dados do cliente

---

### 4. XSS e Conteúdo Dinâmico

**Riscos:**
- Conteúdo pedagógico renderizado
- Inputs administrativos

**Mitigações Iniciais:**
- Escapagem padrão de templates
- CSP restritiva
- Nenhum HTML cru sem sanitização

---

### 5. CSRF e Abuso de Requisições

**Riscos:**
- Ações administrativas forjadas
- Uso indevido de endpoints sensíveis

**Mitigações Iniciais:**
- CSRF obrigatório
- Headers HTMX validados
- Rate limiting

---

### 6. Exposição de Infraestrutura

**Riscos:**
- Vazamento de settings
- DEBUG ativo
- Erros verbosos

**Mitigações Iniciais:**
- DEBUG sempre falso em produção
- Logs controlados
- Separação clara de ambientes

---

### 7. Cadeia de Suprimentos

**Riscos:**
- Dependências vulneráveis
- Atualizações inseguras

**Mitigações Iniciais:**
- Dependências mínimas
- Atualizações conscientes
- Verificação automática

---

## Fora de Escopo v0.1

- Ataques avançados de ML
- Engenharia social
- Ataques físicos

---

**Este documento evolui continuamente.**

Ameaças novas exigem entradas novas.

