import asyncio
from asyncio import run
from aiogram import Dispatcher
from bot import bot
from db.db_requests import clear_left_channels
from routers import start, delete_message, return_to_menu, handle_list_keyboard, handle_y_n_keyboard
from routers.handle_groups import group_join_detect_bot
from routers.menu import get_groups, select_group
from routers.menu.text import get_text, edit_text
from routers.menu.schedule import get_schedule, edit_schedule_date, edit_schedule_time
from routers.menu.default_text import get_default_text, edit_default_text
from routers.menu.group_data import edit_price, edit_amount
from routers.handle_schedule.handle_schedule import run_schedule
import aioschedule as schedule

dp = Dispatcher()


async def main():
    dp.include_routers(
        start.router,
        delete_message.router,
        group_join_detect_bot.router,
        get_groups.router,
        select_group.router,
        return_to_menu.router,
        get_text.router,
        edit_text.router,
        handle_list_keyboard.router,
        handle_y_n_keyboard.router,
        get_default_text.router,
        edit_default_text.router,
        get_schedule.router,
        edit_schedule_date.router,
        edit_schedule_time.router,
        edit_price.router,
        edit_amount.router,
    )
    await clear_left_channels()
    print("Bot running...")
    schedule_task = asyncio.create_task(run_schedule())
    await asyncio.gather(
        dp.start_polling(bot),
        schedule_task
    )


if __name__ == '__main__':
    try:
        run(main())
    except KeyboardInterrupt:
        print("Bot stopped")
