from bot import bot
from db.db_requests import get_channels_by_admin_id, get_all_admins, pop_group_schedule
from string import Template
import aioschedule as schedule
from datetime import datetime
import asyncio
import logging
import json


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
        try:
            if day == int(admin.date) and f"{hour}:{minute}" == admin.time:
                groups = await get_channels_by_admin_id(admin.tgId)
                for group in groups:
                    sched = json.loads(group.schedule)
                    amount = sched[0]
                    pop_group_schedule(group.tgChannelId)
                    price = await calculate_price(int(amount))
                    await bot.send_message(
                        chat_id=group.tgChannelId,
                        text=Template(group.text).substitute(price=price, amount=amount)
                    )
        except ValueError:
            pass
        except Exception as e:
            logging.exception(e)


async def calculate_price(amount: int) -> str:
    if amount < 7:
        price = str(3200)
    elif 7 <= amount < 9:
        price = str(3200)
    elif 9 <= amount < 10:
        price = str(3600)
    elif 10 <= amount <= 12:
        price = str(4000)
    elif 13 <= amount < 14:
        price = str(4300)
    elif amount >= 14:
        price = str(4600)
    else:
        price = str(5000)
    return price
