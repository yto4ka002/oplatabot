import json
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8643705189:AAFhmfrgm7C7-INCVNGEUN6ns4GWMFHzzw8"
DB_FILE = "chats.json"


# ---------- база ----------
def load_chats():
    try:
        with open(DB_FILE, "r") as f:
            return set(json.load(f))
    except:
        return set()


def save_chats(chats):
    with open(DB_FILE, "w") as f:
        json.dump(list(chats), f)


chats = load_chats()


# ---------- логика ----------
def days_until_25():
    today = datetime.now()

    if today.day <= 25:
        target = today.replace(day=25)
    else:
        if today.month == 12:
            target = today.replace(year=today.year + 1, month=1, day=25)
        else:
            target = today.replace(month=today.month + 1, day=25)

    return (target - today).days


# ---------- команды ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    chats.add(chat_id)
    save_chats(chats)

    await update.message.reply_text("Я буду напоминать про оплату 💸")


async def oplata(update: Update, context: ContextTypes.DEFAULT_TYPE):
    days = days_until_25()
    await update.message.reply_text(f"До оплаты осталось {days} дней")


# ---------- рассылка ----------
async def send_notifications(app):
    days = days_until_25()

    if days == 0:
        text = "💸 Сегодня день оплаты!"
    else:
        text = f"📅 До оплаты осталось {days} дней"

    for chat_id in list(chats):
        try:
            await app.bot.send_message(chat_id=chat_id, text=text)
        except:
            pass


# ---------- цикл ----------
async def background_loop(app):
    while True:
        await send_notifications(app)
        await asyncio.sleep(24 * 60 * 60)  # раз в день


# ---------- запуск ----------
import asyncio

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("oplata", oplata))

    # запускаем фоновую задачу
    asyncio.create_task(background_loop(app))

    print("Bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()
