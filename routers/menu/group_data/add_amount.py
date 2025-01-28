from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from bot import bot
from db.db_requests import get_group_schedule, get_user_schedule
from strings.menu_strings import menu_strings
from keyboards.prebuilt import cancel_edit_keyboard, y_n_keyboard
from routers.menu.group_data.get_amount import russian_months
from datetime import datetime

router = Router()


@router.callback_query(F.data == "add_amount")
async def edit_amount(call: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    group_schedule = get_group_schedule(state_data["channel_id"])
    user_schedule = get_user_schedule(call.from_user.id)
    month_now = datetime.now().month
    day_now = datetime.now().date().day
    hour_now = datetime.now().time().hour
    minute_now = datetime.now().time().minute
    if day_now > int(user_schedule["date"]):
        month_now += 1
    elif day_now == int(user_schedule["date"]):
        if hour_now > int(user_schedule["time"].split(":")[0]):
            month_now += 1
        elif hour_now == int(user_schedule["time"].split(":")[0]):
            if minute_now > int(user_schedule["time"].split(":")[1]):
                month_now += 1
    month = russian_months[month_now + len(group_schedule)]
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=state_data["menu_id"],
        text=menu_strings["edit_amount"].substitute(month=month),
        reply_markup=cancel_edit_keyboard
    )
    await state.set_state("enter_amount")


@router.message(StateFilter("enter_amount"))
async def enter_amount(message: Message, state: FSMContext):
    state_data = await state.get_data()
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
    try:
        int(message.text)
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=state_data["menu_id"],
            text=menu_strings["confirm_edit_amount"].substitute(amount=message.text),
            reply_markup=y_n_keyboard
        )
        await state.update_data(amount=message.text)
    except ValueError:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=state_data["menu_id"],
            text=menu_strings["incorrect_amount"],
            reply_markup=cancel_edit_keyboard
        )
