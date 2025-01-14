from aiogram import Router, F
from bot import bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from strings.menu_strings import menu_strings
from keyboards.prebuilt import group_settings_keyboard
from db.db_requests import get_group_name

router = Router()


@router.callback_query(F.data.regexp("group: -\d{1,}"))
@router.callback_query(F.data == "cancel_edit")
async def select_channel(call: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    if not call.data == "cancel_edit":
        channel_id: int = int(call.data.split(" ")[1])
    else:
        channel_id = state_data["channel_id"]
    await state.update_data(channel_id=channel_id)
    menu_id = state_data["menu_id"]
    try:
        await bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=menu_id,
            text=menu_strings["settings"].substitute(title=get_group_name(channel_id)),
            reply_markup=group_settings_keyboard
        )
    except Exception as e:
        msg = await bot.send_message(
            chat_id=call.message.chat.id,
            text=menu_strings["settings"].substitute(title=get_group_name(channel_id)),
            reply_markup=group_settings_keyboard
        )
        await state.update_data(menu_id=msg.message_id)
    await state.set_state(None)
