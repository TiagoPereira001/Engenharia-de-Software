# Como correr o projeto

[Índice](../README.md) · [← Estados e atividades](../05-modelacao/estados-e-atividades.md) · [Estrutura do código →](estrutura.md)

## Com Docker (a forma mais simples)

Só precisas do Docker Desktop aberto. Na pasta do repositório:

```bash
docker compose up --build
```

O `docker-compose.yml` levanta o projeto inteiro, em três contentores na mesma rede:

| Contentor | O que é | Endereço |
|---|---|---|
| `db` | PostgreSQL 16 | só dentro da rede do Docker |
| `backend` | Django com a API | http://localhost:8000/api/ |
| `frontend` | React (Vite) | http://localhost:5173 |

Cada contentor chega aos outros pelo nome (`db`, `backend`). Ao arrancar, o back-end espera que o PostgreSQL esteja pronto, prepara a base de dados e cria os dados de exemplo. Os dados ficam num volume, por isso não se perdem ao parar.

O código está montado dentro dos contentores: quando se guarda um ficheiro em `backend/` ou `frontend/`, o servidor recarrega sozinho e não é preciso reconstruir.

- Parar: `Ctrl+C`, ou `docker compose down` noutro terminal.
- Recomeçar do zero, com a base de dados limpa: `docker compose down -v` e depois `docker compose up --build`.
- Só é preciso `--build` outra vez quando mudam as dependências (`requirements.txt` ou `package.json`).

Com os contentores a correr, noutro terminal:

```bash
docker compose exec backend python manage.py test      # testes do back-end, no PostgreSQL
docker compose exec frontend npm test                  # testes do front-end
docker compose exec backend python manage.py shell     # consola do Django
docker compose exec db psql -U pedidos pedidos         # consola do PostgreSQL
docker compose logs -f backend                         # ver o que o back-end escreve
```

## Sem Docker

Precisas de Python 3.9 ou mais recente e de Node 20 ou mais recente. Sem Docker a base de dados é SQLite (um ficheiro em `backend/`), sem instalar nada.

### Back-end (Django)

```bash
cd backend
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python manage.py migrate
.venv/bin/python manage.py dados_exemplo
.venv/bin/python manage.py runserver
```

O `dados_exemplo` cria cinco utilizadores de teste com o nome das personas (sofia, marta, ricardo, diogo, helena), um por papel, e cinco pedidos. A palavra-passe de cada um é o nome seguido de 123 (`sofia` / `sofia123`). Cria também o administrador `admin` / `admin123`. São contas de teste, só para desenvolvimento.

A API fica em `http://127.0.0.1:8000/api/` e o painel de administração em `/admin/` (entra-se com `admin` / `admin123`).

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
