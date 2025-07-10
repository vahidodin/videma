from fastapi import FastAPI, Request, Depends
from telegram import Update
import uvicorn
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .config import settings
from .bot import setup_bot_handlers
from .database import Base, engine
from telegram.ext import Application

# Create DB tables
Base.metadata.create_all(bind=engine)

# Setup Telegram Bot Application
bot_app = Application.builder().token(settings.telegram_bot_token).build()
setup_bot_handlers(bot_app)

# Setup FastAPI app
app = FastAPI()

# Setup Scheduler
scheduler = AsyncIOScheduler()

async def daily_followup_job():
    """This job runs daily to check for patient followups."""
    # TODO: Add logic to query DB and send followup messages
    print("Executing daily followup check...")
    # Example of sending a message via the bot
    # await bot_app.bot.send_message(chat_id=YOUR_TEST_CHAT_ID, text="This is a scheduled message.")

@app.on_event("startup")
async def startup_event():
    # Setup scheduler
    scheduler.add_job(daily_followup_job, 'cron', hour=9, minute=30)
    scheduler.start()
    
    # Set telegram webhook
    await bot_app.bot.set_webhook(url=f"{settings.webhook_url}/telegram")

@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()

@app.get("/")
async def root():
    return {"message": "Smart Clinic Bot is running"}

@app.post("/telegram")
async def handle_telegram_webhook(request: Request):
    """Handles telegram webhook updates by passing them to the bot app."""
    data = await request.json()

    print("--- ✅ پیام جدید از تلگرام دریافت شد! ---")
    print(data)

    update = Update.de_json(data, bot_app.bot)
    await bot_app.update_queue.put(update)
    return {"status": "ok"}

# To run this app locally for development (without webhook):
# 1. Comment out the `set_webhook` line in `startup_event`.
# 2. Add `asyncio.run(bot_app.run_polling())` at the end of this file (outside any function).
# 3. Run with `uvicorn app.main:app --reload`.
# This will use polling instead of webhooks.