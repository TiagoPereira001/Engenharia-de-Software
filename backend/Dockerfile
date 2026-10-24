# Servidor Django. Usado pelo docker-compose.yml da raiz.
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Ao arrancar: prepara a base de dados, cria os dados de exemplo e liga o servidor (recarrega ao mudar o código).
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py dados_exemplo && python manage.py runserver 0.0.0.0:8000"]
