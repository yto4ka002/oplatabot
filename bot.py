import json
from datetime import datetime, time
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8643705189:AAFhmfrgm7C7-INCVNGEUN6ns4GWMFHzzw8"
DB_FILE = "chats.json"


# ---------- работа с базой ----------
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


# ---------- ежедневная проверка ----------
async def daily_check(context: ContextTypes.DEFAULT_TYPE):
    today = datetime.now()

    if today.day == 25:
        for chat_id in chats:
            try:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text="💸 Сегодня день оплаты!"
                )
            except:
                pass


# ---------- недельное напоминание ----------
async def weekly_notify(context: ContextTypes.DEFAULT_TYPE):
    days = days_until_25()

    for chat_id in chats:
        try:
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"📅 До оплаты осталось {days} дней"
            )
        except:
            pass


# ---------- запуск ----------
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("oplata", oplata))

    job_queue = app.job_queue

    # каждый день в 10:00
    job_queue.run_daily(daily_check, time=time(hour=10, minute=0))

    # раз в 7 дней (каждые 7 суток)
    job_queue.run_repeating(weekly_notify, interval=7 * 24 * 60 * 60, first=10)

    print("Bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()
