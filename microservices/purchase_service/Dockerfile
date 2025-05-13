FROM python:3.11-slim-buster

WORKDIR /app

COPY microservices/purchase_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY microservices/auth_service/. .

EXPOSE 5002

CMD ["python", "app.py"]