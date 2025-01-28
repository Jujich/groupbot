from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from bot import bot
from aiogram.filters import StateFilter
from strings.menu_strings import menu_strings
from keyboards.prebuilt import y_n_keyboard, cancel_keyboard

router = Router()


@router.callback_query(F.data == "groups_send_messages")
async def groups_send_messages(call: CallbackQuery, state: FSMContext):
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=menu_strings["groups_send_messages_1"],
        reply_markup=cancel_keyboard
    )
    await state.set_state("groups_send_messages")


@router.message(StateFilter("groups_send_messages"))
async def groups_send_messages(message: Message, state: FSMContext):
    state_data = await state.get_data()
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
    menu_id = state_data["menu_id"]
    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=menu_id,
        text=menu_strings["groups_send_messages_2"].substitute(text=message.text),
        reply_markup=y_n_keyboard
    )
    await state.update_data(text=message.text)
