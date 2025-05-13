FROM python:3.11-slim-buster

WORKDIR /app

COPY microservices/catalog_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY microservices/auth_service/. .

EXPOSE 5003

CMD ["python", "app.py"]