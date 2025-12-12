from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
import os

# Ваш токен из @BotFather
TOKEN = "8513702327:AAHY_4qf5qbizCXUxlYoOJFgig5CPw6Ovrw"   # ← ваш реальный токен
WEBHOOK_URL = "https://telegram-webhook-e0i9.onrender.com/webhook"       # ← ваш реальный URL

app = FastAPI()

# Эта строка нужна только один раз при первом запуске
@app.on_event("startup")
async def on_startup():
    import requests
    url = f"https://api.telegram.org/bot{TOKEN}/setWebhook"
    requests.post(url, data={"url": WEBHOOK_URL})

# Главный эндпоинт — сюда Telegram будет слать всё
@app.post("/webhook")
async def telegram_webhook(request: Request):
    update = await request.json()
    
    # Просто для теста — бот будет повторять всё, что ему пишут
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")
        
        if text == "/start":
            send_text = "Webhook работает! Я получил твоё сообщение через webhook."
        else:
            send_text = f"Ты написал: {text}"
        
        send_message(chat_id, send_text)
    
    return JSONResponse({"ok": True})

def send_message(chat_id: int, text: str):
    import requests
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

# Для локального тестирования через ngrok
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
