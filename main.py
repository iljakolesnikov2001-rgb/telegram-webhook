from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
import os
import requests  # Убедитесь, что это импортировано (уже добавлено в requirements.txt)

# Ваш токен из @BotFather
TOKEN = "8513702327:AAHY_4qf5qbizCXUxlYoOJFgig5CPw6Ovrw"   # ← ваш реальный токен
WEBHOOK_URL = "https://telegram-webhook-e0i9.onrender.com/webhook"       # ← ваш реальный URL

# Chat ID, куда пересылать сообщения (замените на реальный!)
TARGET_CHAT_ID = 123456789  # ← Вставьте chat_id вашего аккаунта/группы здесь

app = FastAPI()

# Эта строка нужна только один раз при первом запуске
@app.on_event("startup")
async def on_startup():
    print("Сервер стартовал! Webhook готов.", flush=True)  # Добавлено для отладки
    url = f"https://api.telegram.org/bot{TOKEN}/setWebhook"
    response = requests.post(url, data={"url": WEBHOOK_URL})
    print(f"Установка webhook: {response.json()}", flush=True)  # Печатаем ответ от Telegram

# Главный эндпоинт — сюда Telegram будет слать всё
@app.post("/webhook")
async def telegram_webhook(request: Request):
    print("Получен запрос от Telegram!", flush=True)  # Добавлено для отладки
    update = await request.json()
    
    # Для отладки: Печатаем update в логи Render
    print(update, flush=True)
    
    # Обработка сообщения
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        user_id = update["message"]["from"]["id"]
        text = update["message"].get("text", "")
        
        # Пересылаем сообщение в целевой чат
        forward_text = f"Переслано от пользователя {user_id}: {text}"
        send_message(TARGET_CHAT_ID, forward_text)
        
        # Опционально: Отвечаем пользователю эхом (можно удалить, если не нужно)
        if text == "/start":
            send_text = "Webhook работает! Я получил твоё сообщение через webhook."
        else:
            send_text = f"Ты написал: {text}"
        send_message(chat_id, send_text)
    
    return JSONResponse({"ok": True})

def send_message(chat_id: int, text: str):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    response = requests.post(url, json={"chat_id": chat_id, "text": text})
    print(f"Отправка сообщения: {response.json()}", flush=True)  # Добавлено для отладки

# Для локального тестирования через ngrok
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
