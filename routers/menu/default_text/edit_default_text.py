from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from bot import bot
from strings.menu_strings import menu_strings
from keyboards.prebuilt import cancel_edit_default_text_keyboard, y_n_keyboard
from aiogram.filters import StateFilter

router = Router()


@router.callback_query(F.data == "No", StateFilter("enter_default_text"))
@router.callback_query(F.data == "edit_default_text")
async def edit_text(call: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=state_data["menu_id"],
        text=menu_strings["edit_text"],
        reply_markup=cancel_edit_default_text_keyboard
    )
    await state.set_state("enter_default_text")


@router.message(StateFilter("enter_default_text"))
async def enter_text(message: Message, state: FSMContext):
    state_data = await state.get_data()
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
    if "$price" in message.text and "$amount" in message.text:
        text = message.text.replace("$price", "<b>$price</b>").replace("$amount", "<b>$amount</b>")
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=state_data["menu_id"],
            text=menu_strings["confirm_edit_text"].substitute(text=text),
            reply_markup=y_n_keyboard
        )
        await state.update_data(default_text=text)
    else:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=state_data["menu_id"],
            text=menu_strings["text_no_template"],
            reply_markup=cancel_edit_default_text_keyboard
        )
