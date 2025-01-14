from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from db.db_requests import get_default_text
from keyboards.prebuilt import edit_default_text_keyboard
from bot import bot
from strings.menu_strings import menu_strings

router = Router()


@router.callback_query(F.data == "cancel_edit_default")
@router.callback_query(F.data == "get_default_text")
async def get_default_text_cb(call: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    menu_id = state_data["menu_id"]
    default_text = get_default_text(call.from_user.id)
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=menu_id,
        text=menu_strings["text"].substitute(text=default_text),
        reply_markup=edit_default_text_keyboard
    )
    await state.update_data(old_default_text=default_text)
    await state.set_state(None)
