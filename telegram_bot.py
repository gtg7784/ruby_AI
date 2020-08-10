
import argparse
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from train import KoGPT2Chat

load_dotenv(verbose=True)

parser = argparse.ArgumentParser(description='Ruby based on KoGPT-2')

args = parser.parse_args()

model = KoGPT2Chat.load_from_checkpoint(args.model_params)

def start(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="안녕하세요, 저는 당신의 고민을 들어줄 루비에요.")

def echo(bot, update):
  response = model.chat(update.message.text)
  bot.send_message(chat_id=update.message.chat_id, text=response)

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
updater = Updater(token=TELEGRAM_TOKEN)
dispatcher = updater.dispatcher
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

updater.start_polling()
