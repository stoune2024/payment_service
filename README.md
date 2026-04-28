# Async Payment Processing Service

## 📌 Описание

Микросервис для асинхронной обработки платежей.

Сервис:

* принимает запрос на создание платежа
* сохраняет его в БД со статусом `pending`
* публикует событие в очередь (RabbitMQ) через Outbox pattern
* consumer обрабатывает платеж (эмуляция)
* обновляет статус (`succeeded` / `failed`)
* отправляет webhook

---

## 🏗 Архитектура

### Компоненты:

* **API сервис (FastAPI)**
  Обрабатывает HTTP-запросы и работает с БД

* **PostgreSQL**
  Хранение платежей и outbox событий

* **RabbitMQ**
  Асинхронная очередь сообщений

* **Publisher (Outbox worker)**
  Публикует события из таблицы outbox

* **Consumer**
  Обрабатывает платежи

* **Adminer**
  GUI для работы с БД

* **RabbitMQ Management UI**
  GUI для очередей

---

## ⚠️ Архитектурные упрощения

В рамках тестового задания были сделаны следующие упрощения:

### 1. Shared Database

Consumer и API используют одну БД.

👉 В production:

* consumer был бы отдельным сервисом
* не имел бы прямого доступа к БД API

---

### 2. Обновление статуса напрямую из consumer

Сейчас:

* consumer обновляет статус платежа напрямую в БД

👉 В production:

* consumer отправлял бы webhook или событие обратно в API
* API обновлял бы статус через отдельный endpoint

---

### 3. Один сервис вместо нескольких

Сейчас:

* API + processing логика логически разделены, но технически используют одну кодовую базу

👉 В production:

* Payment Service
* Processing Service
* Event Bus между ними

---

### 4. Упрощённая retry логика

* retry реализован на уровне кода

👉 В production:

* использовались бы DLX + TTL в RabbitMQ

---

## 📡 API

### 1. Создание платежа

**POST /api/v1/payments**

Headers:

* `X-API-Key` (обязательный)
* `Idempotency-Key` (обязательный)

Body:

```json
{
  "amount": 100,
  "currency": "USD",
  "description": "test payment",
  "metadata": {"order_id": 123},
  "webhook_url": "http://example.com/webhook"
}
```

Ответ:

```json
{
  "payment_id": "...",
  "status": "pending",
  "created_at": "..."
}
```

---

### 2. Получение платежа

**GET /api/v1/payments/{payment_id}**

Headers:

* `X-API-Key`

Ответ:

```json
{
  "id": "...",
  "amount": 100,
  "currency": "USD",
  "status": "succeeded",
  "created_at": "...",
  "processed_at": "..."
}
```

---

## 🧪 Тестирование API

Я не использую curl.

Вместо этого используется:

👉 **Swagger UI FastAPI**

После запуска:

```
http://localhost:8000/docs
```

Там:

* можно выполнять все запросы
* задавать headers (`X-API-Key`, `Idempotency-Key`)
* удобно смотреть ответы

---

## 🚀 Запуск проекта

### 1. Подготовка

Создать `.env`:

```
DB_HOST=postgres
DB_PORT=5432
DB_USER=postgres
DB_PASS=postgres
DB_NAME=db

API_KEY=test_api_key

BROKER_HOST=rabbitmq
BROKER_PORT=5672
BROKER_USER=guest
BROKER_PASS=guest
```

---

### 2. Запуск

```bash
docker-compose up --build
```

---

### 3. Доступ к сервисам

| Сервис        | URL                        |
| ------------- | -------------------------- |
| API (Swagger) | http://localhost:8000/docs |
| Adminer (БД)  | http://localhost:8080      |
| RabbitMQ UI   | http://localhost:15672     |

---

### 4. Данные для подключения

#### PostgreSQL (Adminer)

* System: PostgreSQL
* Server: postgres
* User: postgres
* Password: postgres
* DB: db

#### RabbitMQ

* login: guest
* password: guest

---

## 🔄 Жизненный цикл платежа

1. Создание платежа → статус `pending`
2. Событие попадает в `outbox`
3. Publisher отправляет в `payment.new`
4. Consumer:

   * ждёт 2–5 секунд
   * с вероятностью:

     * 90% → `succeeded`
     * 10% → `failed`
5. Обновляет БД
6. Отправляет webhook

---

## ✅ Реализовано

* FastAPI + Pydantic v2
* Async SQLAlchemy 2.0
* PostgreSQL
* RabbitMQ (FastStream)
* Outbox pattern
* Idempotency
* Retry логика
* DLQ (базовая)
* Docker Compose
* Swagger UI
* Adminer + RabbitMQ UI

---

## 📌 Возможные улучшения

* Разделение на 2 микросервиса
* Event-driven обновление статуса
* DLX + TTL retry
* Idempotent consumer
* Monitoring (Prometheus)
* Structured logging

---

## 🧠 Итог

Проект реализует ключевые паттерны:

* асинхронная обработка
* гарантированная доставка событий
* идемпотентность
* отказоустойчивость

При этом архитектура упрощена осознанно для соответствия объёму тестового задания.
