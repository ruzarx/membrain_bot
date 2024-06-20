import sys
sys.path.append('.')
sys.path.append('..')


from datetime import datetime, timedelta
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler

from data_structures import ReminderRecord
from postgres_connector import DBConnect

BOT_TOKEN = '7051366834:AAGw3qHvgXvSu27het4HRo97T5C2cTd3Fnk'
FLASK_API_URL = 'http://membrain_bot-flask-1:5000/'


db = DBConnect()
table = 'users.reminders'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_id = update.effective_chat.id
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"User id {user_id}")
    print(f"User {user_message}")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"User message {user_message}")
    response = requests.post(FLASK_API_URL, json={'query': user_message})
    if response.status_code == 200:
        prediction = response.json()['prediction']
    else:
        prediction = "No prediction"

    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Prediction {prediction}")
    reminder_date = datetime.now() + timedelta(days=2, hours=2)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"User message {user_message}, {type(user_message)}")
    record = ReminderRecord(user_id=user_id,
                            query_txt=user_message,
                            reminder_txt=prediction,
                            reminder_date=reminder_date)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=record.__repr__())
    db.insert_data(table, record)
    print("DATA RECORDED")
    df = db.read_data(table, user_id=user_id)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=df[['user_id',
                                                             'query_txt',
                                                             'reminder_txt',
                                                             'reminder_date']].__repr__())


if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    
    application.run_polling()
