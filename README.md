# Coreano Marcial - Fase 0

Sistema de ensino de idioma coreano contextualizado para artes marciais.

## Stack Técnico

- Backend: Django 4.2
- Banco de dados: PostgreSQL
- Frontend: HTML + CSS (sem HTMX na Fase 0)

## Requisitos

- Python 3.10+
- PostgreSQL 14+

## Instalação

1. Clone o repositório:
```bash
git clone <repository-url>
cd coreano-marcial
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite .env com suas configurações
```

5. Crie o banco de dados PostgreSQL:
```bash
createdb coreano_marcial
```

6. Execute as migrações:
```bash
python manage.py makemigrations
python manage.py migrate
```

7. Crie um superusuário:
```bash
python manage.py createsuperuser
```

8. Crie o diretório de logs:
```bash
mkdir logs
```

9. Execute o servidor de desenvolvimento:
```bash
python manage.py runserver
```

10. Acesse:
- Interface: http://localhost:8000/
- Admin: http://localhost:8000/admin/

## Estrutura do Projeto

```
coreano-marcial/
├── config/              # Configurações do Django
├── apps/
│   ├── users/          # Autenticação e usuários
│   ├── lessons/        # Lições e vocabulário
│   ├── progress/       # Progresso do usuário
│   └── audio/          # Gerenciamento de áudio
├── templates/          # Templates HTML
├── static/             # Arquivos estáticos (CSS)
├── media/              # Uploads (áudio)
├── logs/               # Logs da aplicação
├── manage.py
├── requirements.txt
└── .env.example
```

## Uso

1. Acesse o Django Admin (`/admin/`)
2. Adicione níveis de faixa (BeltLevel)
3. Adicione lições para cada faixa
4. Adicione vocabulário e associe às lições
5. Faça upload de arquivos de áudio
6. Usuários podem se registrar e começar a aprender

## Fase 0 - Limitações

- Nenhuma interatividade HTMX (páginas recarregam completamente)
- Nenhum modo offline (PWA será na Fase 2)
- Nenhum pronunciation assessment (Fase 3)
- Gerenciamento de conteúdo via Django Admin

## Próximas Fases

- **Fase 1**: HTMX para partial rendering
- **Fase 2**: Service Worker + PWA offline mode
- **Fase 3**: Pronunciation Assessment API integration

## Pull Request & Governance

Antes de abrir PRs que alterem `docs/PRD.md` ou specs, siga este processo:

1. Preencha a seção `Constitution Compliance` no seu spec (ou no corpo do PR) indicando a(s) seção(ões) do `docs/PRD.md` relacionadas.
2. Inclua um `Sync Impact Report` no corpo do PR (veja `.github/PULL_REQUEST_TEMPLATE.md`).
3. Nomeie um `Designated Reviewer` (pedagogia/conteúdo ou segurança, conforme o caso).
4. Para alterações que impactam segurança/privacidade, atualize `docs/threats_v_0.md` e solicite revisão de segurança antes do merge.
5. Obtenha aprovações: 1 Maintainer + 1 Designated Reviewer (ou follow-up independente para MAJOR changes).

Comandos úteis para criar a PR localmente (substitua `<remote-url>` se necessário):

```bash
git remote add origin <remote-url>
git push -u origin 001-add-prd
# com GitHub CLI:
gh pr create --base main --head 001-add-prd --title "docs: add PRD + governance" --body-file .github/PULL_REQUEST_TEMPLATE.md
```

## Segurança

- SECRET_KEY em variável de ambiente
- DEBUG=False em produção
- HTTPS obrigatório em produção
- CSRF protection ativo
- CSP headers configurados
- Session cookies seguras

## Licença

[Adicionar licença apropriada]
