# Como correr o projeto

[Índice](../README.md) · [← Estados e atividades](../05-modelacao/estados-e-atividades.md) · [Estrutura do código →](estrutura.md)

Precisas de Python 3.9 ou mais recente e de Node 20 ou mais recente.

## Back-end (Django)

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

## Front-end (React)

Noutro terminal, com o back-end a correr:

```bash
cd frontend
npm install
npm run dev
```

Abre `http://localhost:5173`. O Vite reencaminha `/api` para o Django, por isso a sessão funciona sem configuração extra.

## Variáveis de ambiente

Os valores sensíveis vêm de variáveis de ambiente. O modelo está em `backend/.env.example`. O `.env` verdadeiro nunca vai para o Git.

## Ver também

- [Estrutura do código](estrutura.md)
- [Testes](testes.md)
