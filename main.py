from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties

import asyncio

from postgres_connector import DBConnect
from data_structures import ReminderRecord

db = DBConnect()


parse_mode = ParseMode.HTML
default_bot_properties = DefaultBotProperties(parse_mode=parse_mode)
bot = Bot(
    token='7051366834:AAGw3qHvgXvSu27het4HRo97T5C2cTd3Fnk',
    default=default_bot_properties
    )


table = 'users.reminders'

dispatcher = Dispatcher()



@dispatcher.message()
async def echo(message: Message):
    reminder_date = datetime.now() + timedelta(days=2, hours=2)
    record = ReminderRecord(user_id=message.from_user.id,
                            reminder_txt=f"Processed message {message.text}",
                            reminder_date=reminder_date)
    db.insert_data(table, record)
    print("DATA RECORDED")
    df = db.read_data(table, user_id=message.from_user.id)
    await message.answer(text=df[['user_id', 'reminder_txt', 'reminder_date']].__repr__())


async def start():
    await dispatcher.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(start())


