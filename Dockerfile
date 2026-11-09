FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY config.py init_db.py start.sh ./

RUN chmod 755 start.sh && mkdir -p /app/instance/data

EXPOSE 5000
CMD ["./start.sh"]
