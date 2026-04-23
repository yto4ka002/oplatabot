import asyncio
import json
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "ТВОЙ_ТОКЕН"

# файл где храним чаты
DB_FILE = "chats.json"


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


# команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    chats.add(chat_id)
    save_chats(chats)

    await update.message.reply_text(
        "Я буду напоминать про оплату 💸"
    )


# команда /oplata
async def oplata(update: Update, context: ContextTypes.DEFAULT_TYPE):
    days = days_until_25()
    await update.message.reply_text(
        f"До оплаты осталось {days} дней"
    )


# рассылка
async def weekly_notify(app):
    while True:
        days = days_until_25()
        for chat_id in chats:
            try:
                await app.bot.send_message(
                    chat_id=chat_id,
                    text=f"До оплаты осталось {days} дней"
                )
            except:
                pass
        await asyncio.sleep(7 * 24 * 60 * 60)


async def daily_check(app):
    while True:
        today = datetime.now()
        if today.day == 25:
            for chat_id in chats:
                try:
                    await app.bot.send_message(
                        chat_id=chat_id,
                        text="💸 Сегодня день оплаты!"
                    )
                except:
                    pass
        await asyncio.sleep(24 * 60 * 60)


async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("oplata", oplata))

    asyncio.create_task(weekly_notify(app))
    asyncio.create_task(daily_check(app))

    await app.run_polling()


if name == "__main__":
    asyncio.run(main())
