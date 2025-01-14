from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
from aiogram import Bot
import os

load_dotenv("config.env")

try:
    bot = Bot(token=str(os.environ.get("TOKEN")), default=DefaultBotProperties(parse_mode='HTML'))
except Exception as e:
    print("Unable to start bot: ", e)
