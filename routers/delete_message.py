from aiogram.types import CallbackQuery
from bot import bot
from aiogram import Router, F

router = Router()


@router.callback_query(F.data == "delete_message")
async def group_handle_message(call: CallbackQuery):
    await bot.delete_message(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
    )
