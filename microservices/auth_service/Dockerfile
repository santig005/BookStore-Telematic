FROM python:3.11-slim-buster

WORKDIR /app

COPY microservices/auth_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5001

CMD ["python", "app.py"]