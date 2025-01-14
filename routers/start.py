from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from strings.message_strings import message_strings
from keyboards.prebuilt import start_keyboard
from bot import bot
from db.db_requests import insert_admin
from aiogram.fsm.context import FSMContext

router = Router()


@router.message(Command("start"))
async def start(message: Message, state: FSMContext, main=True):
    if message.chat.type == "private":
        if main:
            data = {
                "tgId": message.from_user.id,
                "username": message.from_user.username,
            }
            insert_admin(data)
            msg = await bot.send_message(
                chat_id=message.chat.id,
                text=message_strings["start"],
                reply_markup=start_keyboard
            )
            await state.update_data(menu_id=msg.message_id)
        else:
            try:
                state_data = await state.get_data()
                menu_id = state_data["menu_id"]
                await bot.edit_message_text(
                    text=message_strings["start"],
                    chat_id=message.chat.id,
                    message_id=menu_id,
                    reply_markup=start_keyboard
                )
            except:
                msg = await bot.send_message(
                    text=message_strings["start"],
                    chat_id=message.chat.id,
                    reply_markup=start_keyboard
                )
                await state.update_data(menu_id=msg.message_id)
    await state.set_state(None)
