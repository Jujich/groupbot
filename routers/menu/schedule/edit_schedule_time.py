from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from bot import bot
from keyboards.prebuilt import cancel_edit_schedule_keyboard, y_n_keyboard
from strings.menu_strings import menu_strings
from aiogram.filters import StateFilter
from datetime import datetime

router = Router()


@router.callback_query(F.data == "No", StateFilter("enter_schedule_time"))
@router.callback_query(F.data == "edit_schedule_time")
async def edit_schedule(call: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=state_data["menu_id"],
        text=menu_strings["edit_schedule_time"],
        reply_markup=cancel_edit_schedule_keyboard
    )
    await state.set_state("enter_schedule_time")


@router.message(StateFilter("enter_schedule_time"))
async def enter_text(message: Message, state: FSMContext):
    state_data = await state.get_data()
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
    try:
        datetime.strptime(message.text, "%H:%M")
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=state_data["menu_id"],
            text=menu_strings["confirm_edit_schedule"].substitute(text=message.text),
            reply_markup=y_n_keyboard
        )
        await state.update_data(time=message.text)
    except ValueError:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=state_data["menu_id"],
            text=menu_strings["incorrect_time"],
            reply_markup=cancel_edit_schedule_keyboard
        )
