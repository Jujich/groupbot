from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from bot import bot
from strings.menu_strings import menu_strings
from keyboards.prebuilt import cancel_edit_keyboard, y_n_keyboard
from aiogram.filters import StateFilter

router = Router()


@router.callback_query(F.data == "No", StateFilter("enter_price"))
@router.callback_query(F.data == "edit_price")
async def edit_price(call: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=state_data["menu_id"],
        text=menu_strings["edit_price"],
        reply_markup=cancel_edit_keyboard
    )
    await state.set_state("enter_price")


@router.message(StateFilter("enter_price"))
async def enter_price(message: Message, state: FSMContext):
    state_data = await state.get_data()
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
    price = message.text.replace(",", ".")
    try:
        float(price)
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=state_data["menu_id"],
            text=menu_strings["confirm_edit_price"].substitute(price=price),
            reply_markup=y_n_keyboard
        )
        await state.update_data(price=price)
    except ValueError:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=state_data["menu_id"],
            text=menu_strings["incorrect_price"],
            reply_markup=cancel_edit_keyboard
        )
