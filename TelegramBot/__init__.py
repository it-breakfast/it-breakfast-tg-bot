from TelegramBot import config

from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from TelegramBot.helpers.cron import scheduled_job, check_last_message
from pytz import timezone 
from telethon.sync import TelegramClient

bot_token=config.BOT_TOKEN
api_id = config.API_ID
api_hash = config.API_HASH
phone = config.BOT_NAME

client_userbot = TelegramClient(phone, api_id, api_hash)

bot = Bot(bot_token)
dp  = Dispatcher()

scheduler = AsyncIOScheduler(timezone="Asia/Bangkok")
scheduler.add_job(scheduled_job, CronTrigger(day_of_week='wed', hour=12, minute=0, timezone=timezone("Asia/Bangkok")), kwargs={"bot": bot}, )
scheduler.add_job(check_last_message, CronTrigger(minute='*/10', timezone=timezone("Asia/Bangkok")), kwargs={"bot": bot})
