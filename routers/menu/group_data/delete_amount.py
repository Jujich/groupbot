from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from bot import bot
from strings.menu_strings import menu_strings
from keyboards.prebuilt import y_n_keyboard
from db.db_requests import get_group_schedule
from routers.menu.group_data.get_amount import russian_months
from datetime import datetime

router = Router()


@router.callback_query(F.data == "delete_amount")
async def delete_amount(call: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    group_schedule = get_group_schedule(state_data["channel_id"])
    month = russian_months[datetime.now().month + len(group_schedule)]
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=menu_strings["delete_amount"].substitute(month=month),
        reply_markup=y_n_keyboard
    )
    await state.set_state("delete_amount")
