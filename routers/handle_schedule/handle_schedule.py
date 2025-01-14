from bot import bot
from db.db_requests import get_channels_by_admin_id, get_all_admins
from string import Template
import aioschedule as schedule
from datetime import datetime
import asyncio


async def run_schedule():
    schedule.every(60).seconds.do(send_messages)
    while True:
        jobs = schedule.jobs
        tasks = [asyncio.create_task(job.run()) for job in jobs]
        if tasks:
            await asyncio.wait(tasks)
        await schedule.run_pending()
        await asyncio.sleep(60)


async def send_messages():
    admins = await get_all_admins()
    day = datetime.now().date().day
    hour = datetime.now().time().hour
    minute = datetime.now().time().minute
    for admin in admins:
        if day == int(admin.date) and f"{hour}:{minute}" == admin.time:
            groups = await get_channels_by_admin_id(admin.tgId)
            for group in groups:
                await bot.send_message(
                    chat_id=group.tgChannelId,
                    text=Template(group.text).substitute(price=group.price, amount=group.amount)
                )
