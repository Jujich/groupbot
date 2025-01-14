from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


def build_inline_list_keyboard(buttons: list[InlineKeyboardButton]) -> list[InlineKeyboardMarkup]:
    keyboards = []
    builder = InlineKeyboardBuilder()
    counter = 0
    first_iter = True
    for item in buttons:
        counter += 1
        if counter == 9:
            if first_iter:
                if len(buttons) > 8:
                    builder.row(
                        InlineKeyboardButton(text=">>>", callback_data="right")
                    )
                first_iter = False
            else:
                builder.row(
                    InlineKeyboardButton(text="<<<", callback_data="left"),
                    InlineKeyboardButton(text=">>>", callback_data="right")
                )
            builder.row(InlineKeyboardButton(text="Отмена", callback_data="cancel"))
            keyboards.append(builder.as_markup())
            builder = InlineKeyboardBuilder()
            counter = 0
        builder.row(item)
    if len(buttons) > 8:
        builder.row(
            InlineKeyboardButton(text="<<<", callback_data="left")
        )
    builder.row(InlineKeyboardButton(text="Отмена", callback_data="cancel"))
    keyboards.append(builder.as_markup())
    return keyboards


def build_confirmation_keyboard(user_id: int, chat_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="confirm", callback_data=f"confirm: {user_id} chat: {chat_id}"),
        InlineKeyboardButton(text="deny", callback_data=f"deny: {user_id} chat: {chat_id}")
    )
    print(f"confirm: {user_id} chat: {chat_id}")
    return builder.as_markup()
