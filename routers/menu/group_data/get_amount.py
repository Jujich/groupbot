from datetime import datetime
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from bot import bot
from strings.menu_strings import menu_strings
from keyboards.prebuilt import edit_amount_keyboard
from aiogram.filters import StateFilter
from db.db_requests import get_group_schedule, get_user_schedule
from routers.handle_schedule.handle_schedule import calculate_price

router = Router()


russian_months = {
    1: "Январь",
    2: "Февраль",
    3: "Март",
    4: "Апрель",
    5: "Май",
    6: "Июнь",
    7: "Июль",
    8: "Август",
    9: "Сентябрь",
    10: "Октябрь",
    11: "Ноябрь",
    12: "Декабрь"
}


async def prepare_group_schedule(schedule: list, admin_id: int) -> str:
    res = ""
    i = datetime.now().month
    user_schedule = get_user_schedule(admin_id)
    day_now = datetime.now().date().day
    hour_now = datetime.now().time().hour
    minute_now = datetime.now().time().minute
    if day_now > int(user_schedule["date"]):
        i += 1
    elif day_now == int(user_schedule["date"]):
        if hour_now > int(user_schedule["time"].split(":")[0]):
            i += 1
        elif hour_now == int(user_schedule["time"].split(":")[0]):
            if minute_now > int(user_schedule["time"].split(":")[1]):
                i += 1
    for item in schedule:
        if i > 12:
            i = 1
        price = await calculate_price(int(item))
        res += f"<b>{russian_months[i]}:</b>\nЗанятий: {item}, Цена: {price}\n\n"
        i += 1
    if len(res) == 0:
        res = "Расписание не задано"
    return res


@router.callback_query(F.data == "No", StateFilter("enter_amount"))
@router.callback_query(F.data == "No", StateFilter("delete_amount"))
@router.callback_query(F.data == "get_amount")
async def get_amount(call: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    schedule = get_group_schedule(state_data["channel_id"])
    res_schedule = await prepare_group_schedule(schedule, call.from_user.id)
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=state_data["menu_id"],
        text=menu_strings["get_amount"].substitute(schedule=res_schedule),
        reply_markup=edit_amount_keyboard
    )
    await state.set_state(None)
