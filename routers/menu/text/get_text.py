from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from db.db_requests import get_group_text, get_group_data
from keyboards.prebuilt import edit_text_keyboard
from bot import bot
from strings.menu_strings import menu_strings

router = Router()


@router.callback_query(F.data == "get_text")
async def get_text(call: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    menu_id = state_data["menu_id"]
    group_data = get_group_data(state_data["channel_id"])
    text = get_group_text(state_data["channel_id"]).substitute(price=group_data["price"], amount=group_data["amount"])
    if text:
        await bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=menu_id,
            text=menu_strings["text"].substitute(text=text),
            reply_markup=edit_text_keyboard
        )
    else:
        await bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=menu_id,
            text=menu_strings["text"].substitute(text=menu_strings["default_text"]),
            reply_markup=edit_text_keyboard
        )
    await state.update_data(old_text=text)
