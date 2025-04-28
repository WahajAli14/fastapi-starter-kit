FROM python:3.11-slim AS builder

WORKDIR /install

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir --prefix=/install/deps -r requirements.txt

FROM python:3.11-slim

RUN adduser --disabled-password --no-create-home appuser

WORKDIR /app

COPY --from=builder /install/deps /usr/local

COPY app/. .

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

USER appuser

EXPOSE 8000

CMD ["fastapi", "dev", "main.py", "--port", "8000", "--host", "0.0.0.0"]

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
