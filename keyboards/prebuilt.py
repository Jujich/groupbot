from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from strings.keyboard_strings import keyboard_strings
import os
from dotenv import load_dotenv

load_dotenv("config.env")


builder = InlineKeyboardBuilder()
builder.row(
    InlineKeyboardButton(text=keyboard_strings["get_groups"], callback_data="get_groups"),
)
builder.row(
    InlineKeyboardButton(text=keyboard_strings["get_default_text"], callback_data="get_default_text"),
    InlineKeyboardButton(text=keyboard_strings["get_schedule"], callback_data="get_schedule"),
)
builder.row(
    InlineKeyboardButton(
        text=keyboard_strings["add_group"],
        callback_data="add_group",
        url=f"https://t.me/{os.environ.get('BOT_USERNAME')}?startgroup=newgroups&admin=manage_chat+change_info+delete_messages+restrict_members+invite_users+promote_members"
    ),
)
start_keyboard = builder.as_markup()


builder = InlineKeyboardBuilder()
builder.row(
    InlineKeyboardButton(text="Удалить это сообщение", callback_data="delete_message"),
)
delete_message_keyboard = builder.as_markup()


builder = InlineKeyboardBuilder()
builder.row(
    InlineKeyboardButton(text=keyboard_strings["get_text"], callback_data="get_text"),
)
builder.row(
    InlineKeyboardButton(text=keyboard_strings["back"], callback_data="cancel_settings"),
)
group_settings_keyboard = builder.as_markup()


builder = InlineKeyboardBuilder()
builder.row(
    InlineKeyboardButton(text=keyboard_strings["edit_text"], callback_data="edit_text"),
)
builder.row(
    InlineKeyboardButton(text=keyboard_strings["edit_amount"], callback_data="edit_amount"),
    InlineKeyboardButton(text=keyboard_strings["edit_price"], callback_data="edit_price"),
)
builder.row(
    InlineKeyboardButton(text=keyboard_strings["cancel_edit"], callback_data="cancel_edit"),
)
edit_text_keyboard = builder.as_markup()


builder = InlineKeyboardBuilder()
builder.row(
    InlineKeyboardButton(text=keyboard_strings["cancel_edit"], callback_data="cancel_edit"),
)
cancel_edit_keyboard = builder.as_markup()


builder = InlineKeyboardBuilder()
builder.row(
    InlineKeyboardButton(text=keyboard_strings["edit_time"], callback_data="edit_schedule_time"),
    InlineKeyboardButton(text=keyboard_strings["edit_date"], callback_data="edit_schedule_date"),
)
builder.row(
    InlineKeyboardButton(text=keyboard_strings["cancel_edit"], callback_data="cancel"),
)
edit_schedule_keyboard = builder.as_markup()


builder = InlineKeyboardBuilder()
builder.row(
    InlineKeyboardButton(text=keyboard_strings["edit"], callback_data="edit_default_text"),
    InlineKeyboardButton(text=keyboard_strings["cancel_edit"], callback_data="cancel"),
)
edit_default_text_keyboard = builder.as_markup()


builder = InlineKeyboardBuilder()
builder.row(
    InlineKeyboardButton(text=keyboard_strings["cancel_edit"], callback_data="cancel_edit_default"),
)
cancel_edit_default_text_keyboard = builder.as_markup()


builder = InlineKeyboardBuilder()
builder.row(
    InlineKeyboardButton(text=keyboard_strings["cancel_edit"], callback_data="cancel_edit_schedule"),
)
cancel_edit_schedule_keyboard = builder.as_markup()


builder = InlineKeyboardBuilder()
builder.add(
    InlineKeyboardButton(text="Да", callback_data="Yes"),
    InlineKeyboardButton(text="Нет", callback_data="No")
)
y_n_keyboard = builder.as_markup()
