from aiogram import Router, F
from keyboards.keyboard_builder import build_inline_list_keyboard
from bot import bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton
from db.db_requests import get_channels_by_admin_id
from strings.menu_strings import menu_strings

router = Router()


@router.callback_query(F.data == "get_groups")
async def get_channels(call: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    menu_id = state_data["menu_id"]
    channels = await get_channels_by_admin_id(call.from_user.id)
    channel_buttons = []
    for item in channels:
        channel_buttons.append(
            InlineKeyboardButton(
                text=item.title,
                callback_data="group: " + str(item.tgChannelId)
            )
        )
    channel_keyboard = build_inline_list_keyboard(channel_buttons)
    await state.update_data(channel_keyboard=channel_keyboard, current=0)
    try:
        await bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=menu_id,
            text=menu_strings["get_groups"],
            reply_markup=channel_keyboard[0],
        )
    except:
        msg = await bot.send_message(
            chat_id=call.message.chat.id,
            text=menu_strings["get_groups"],
            reply_markup=channel_keyboard[0],
        )
        await state.update_data(menu_id=msg.message_id)
