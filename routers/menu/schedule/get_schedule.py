from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from db.db_requests import get_user_schedule
from keyboards.prebuilt import edit_schedule_keyboard
from bot import bot
from strings.menu_strings import menu_strings

router = Router()


@router.callback_query(F.data == "cancel_edit_schedule")
@router.callback_query(F.data == "get_schedule")
async def get_schedule(call: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    menu_id = state_data["menu_id"]
    schedule = get_user_schedule(call.from_user.id)
    if schedule:
        await bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=menu_id,
            text=menu_strings["schedule"].substitute(date=schedule["date"], time=schedule["time"]),
            reply_markup=edit_schedule_keyboard
        )
    else:
        await bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=menu_id,
            text=menu_strings["schedule"].substitute(schedule=menu_strings["default_schedule"]),
            reply_markup=edit_schedule_keyboard
        )
    await state.update_data(old_schedule=schedule)
