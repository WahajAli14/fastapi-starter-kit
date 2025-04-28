FROM python:3.11-slim AS builder

WORKDIR /install

COPY requirements.txt . 

RUN pip install --upgrade pip \
    && pip install --no-cache-dir --prefix=/install/deps -r requirements.txt

FROM python:3.11-slim

RUN adduser --disabled-password --no-create-home workeruser

WORKDIR /worker

COPY --from=builder /install/deps /usr/local

COPY worker/. .

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

USER workeruser

CMD ["python", "worker_main.py"]
