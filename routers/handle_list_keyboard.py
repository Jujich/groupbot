from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from bot import bot
from strings.menu_strings import menu_strings

router = Router()


@router.callback_query(F.data.in_(["right", "left"]))
async def handle_list_keyboard(call: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    if call.data == "right":
        await bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=state_data["menu_id"],
            text=menu_strings["get_groups"],
            reply_markup=state_data["channel_keyboard"][state_data["current"] + 1]
        )
        await state.update_data(current=state_data["current"] + 1)
    elif call.data == "left":
        await bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=state_data["menu_id"],
            text=menu_strings["get_groups"],
            reply_markup=state_data["channel_keyboard"][state_data["current"] - 1]
        )
        await state.update_data(current=state_data["current"] - 1)
