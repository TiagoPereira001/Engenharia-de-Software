# Como correr o projeto

[Índice](../README.md) · [← Estados e atividades](../05-modelacao/estados-e-atividades.md) · [Estrutura do código →](estrutura.md)

## Com Docker (a forma mais simples)

Só precisas do Docker Desktop aberto. Na pasta do repositório:

```bash
docker compose up --build
```

O `docker-compose.yml` levanta dois contentores na mesma rede:

| Contentor | O que é | Endereço |
|---|---|---|
| `backend` | Django com a API | http://localhost:8000/api/ |
| `frontend` | React (Vite) | http://localhost:5173 |

O front-end chega ao back-end pelo nome `backend`, dentro da rede do Docker. Ao arrancar, o back-end prepara a base de dados e cria os dados de exemplo (só da primeira vez). A base de dados fica num volume, por isso não se perde ao parar.

- Parar: `Ctrl+C`, ou `docker compose down` noutro terminal.
- Recomeçar do zero, com a base de dados limpa: `docker compose down -v` e depois `docker compose up --build`.
- Depois de mudar código ou dependências, voltar a correr com `--build`.

## Sem Docker

Precisas de Python 3.9 ou mais recente e de Node 20 ou mais recente.

### Back-end (Django)

```bash
cd backend
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python manage.py migrate
.venv/bin/python manage.py dados_exemplo
.venv/bin/python manage.py runserver
```

O `dados_exemplo` cria cinco utilizadores de teste com o nome das personas (sofia, marta, ricardo, diogo, helena), um por papel, e cinco pedidos. A palavra-passe de teste está em `backend/pedidos/management/commands/dados_exemplo.py`. Só serve para desenvolvimento.

A API fica em `http://127.0.0.1:8000/api/` e o painel de administração em `/admin/` (para entrar no painel cria um superutilizador com `manage.py createsuperuser`).

### Front-end (React)

Noutro terminal, com o back-end a correr:

```bash
cd frontend
npm install
npm run dev
```

Abre `http://localhost:5173`. O Vite reencaminha `/api` para o Django (ou para o contentor `backend`, no Docker, através de `API_URL`). O Django confia nessa origem para aceitar os pedidos POST (`DJANGO_CSRF_TRUSTED_ORIGINS`).

## Variáveis de ambiente

Os valores sensíveis vêm de variáveis de ambiente. O modelo está em `backend/.env.example`. O `.env` verdadeiro nunca vai para o Git.

## Ver também

- [Estrutura do código](estrutura.md)
- [Testes](testes.md)
