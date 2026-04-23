import asyncio
from datetime import datetime
from telegram import Bot

TOKEN = "8643705189:AAFhmfrgm7C7-INCVNGEUN6ns4GWMFHzzw8"
CHAT_ID = 1081004631  

bot = Bot(token=TOKEN)

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

async def weekly_notify():
    while True:
        days = days_until_25()
        await bot.send_message(
            chat_id=CHAT_ID,
            text=f"До оплаты осталось {days} дней"
        )
        await asyncio.sleep(7 * 24 * 60 * 60)

async def daily_check():
    while True:
        today = datetime.now()
        if today.day == 25:
            await bot.send_message(
                chat_id=CHAT_ID,
                text="💸 Сегодня день оплаты!"
            )
        await asyncio.sleep(24 * 60 * 60)

async def main():
    await asyncio.gather(
        weekly_notify(),
        daily_check()
    )

asyncio.run(main())
