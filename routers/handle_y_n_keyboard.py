from bot import bot
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from strings.menu_strings import menu_strings
from keyboards.prebuilt import edit_text_keyboard, edit_default_text_keyboard, edit_schedule_keyboard
from db.db_requests import (update_group_text,
                            update_default_text,
                            get_channels_by_admin_id,
                            update_schedule_time,
                            update_schedule_date,
                            update_group_price,
                            update_group_amount,
                            get_group_data,
                            get_group_text)
from string import Template

router = Router()


@router.callback_query(F.data.in_(["Yes"]))
async def handle_y_n_keyboard(call: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    state_state = await state.get_state()
    if call.data == "Yes":
        if state_state == "enter_text":
            if update_group_text(state_data["channel_id"], state_data["text"]):
                text = Template(state_data["text"])
                await call.answer(
                    show_alert=True,
                    text=menu_strings["edit_text_success"]
                )
            else:
                text = Template(state_data["old_text"])
                await call.answer(
                    show_alert=True,
                    text=menu_strings["edit_text_failure"]
                )
            group_data = get_group_data(state_data["channel_id"])
            text = text.substitute(price=group_data["price"], amount=group_data["amount"])
            await bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=state_data["menu_id"],
                text=menu_strings["text"].substitute(text=text),
                reply_markup=edit_text_keyboard
            )
        elif state_state == "enter_default_text":
            if update_default_text(call.from_user.id, state_data["default_text"]):
                for group in await get_channels_by_admin_id(call.from_user.id):
                    update_group_text(group.tgChannelId, state_data["default_text"])
                text = state_data["default_text"]
                await call.answer(
                    show_alert=True,
                    text=menu_strings["edit_text_success"]
                )
            else:
                text = state_data["old_default_text"]
                await call.answer(
                    show_alert=True,
                    text=menu_strings["edit_text_failure"]
                )
            await bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=state_data["menu_id"],
                text=menu_strings["text"].substitute(text=text),
                reply_markup=edit_default_text_keyboard
            )
        elif state_state == "enter_schedule_date":
            schedule = state_data["old_schedule"]
            if update_schedule_date(call.from_user.id, state_data["date"]):
                schedule["date"] = state_data["date"]
                await call.answer(
                    show_alert=True,
                    text=menu_strings["edit_text_success"]
                )
            else:
                await call.answer(
                    show_alert=True,
                    text=menu_strings["edit_text_failure"]
                )
            await bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=state_data["menu_id"],
                text=menu_strings["schedule"].substitute(date=schedule["date"], time=schedule["time"]),
                reply_markup=edit_schedule_keyboard
            )
        elif state_state == "enter_schedule_time":
            schedule = state_data["old_schedule"]
            if update_schedule_time(call.from_user.id, state_data["time"]):
                schedule["time"] = state_data["time"]
                await call.answer(
                    show_alert=True,
                    text=menu_strings["edit_text_success"]
                )
            else:
                await call.answer(
                    show_alert=True,
                    text=menu_strings["edit_text_failure"]
                )
            await bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=state_data["menu_id"],
                text=menu_strings["schedule"].substitute(date=schedule["date"], time=schedule["time"]),
                reply_markup=edit_schedule_keyboard
            )
        elif state_state == "enter_price":
            group_data = get_group_data(state_data["channel_id"])
            if update_group_price(state_data["channel_id"], state_data["price"]):
                group_data["price"] = state_data["price"]
                await call.answer(
                    show_alert=True,
                    text=menu_strings["edit_text_success"]
                )
            else:
                await call.answer(
                    show_alert=True,
                    text=menu_strings["edit_text_failure"]
                )
            text = get_group_text(state_data["channel_id"]).substitute(price=group_data["price"],
                                                            amount=group_data["amount"])
            await bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=state_data["menu_id"],
                text=menu_strings["text"].substitute(text=text),
                reply_markup=edit_text_keyboard
            )
        elif state_state == "enter_amount":
            group_data = get_group_data(state_data["channel_id"])
            if update_group_amount(state_data["channel_id"], state_data["amount"]):
                group_data["amount"] = state_data["amount"]
                await call.answer(
                    show_alert=True,
                    text=menu_strings["edit_text_success"]
                )
            else:
                await call.answer(
                    show_alert=True,
                    text=menu_strings["edit_text_failure"]
                )
            text = get_group_text(state_data["channel_id"]).substitute(price=group_data["price"],
                                                                       amount=group_data["amount"])
            await bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=state_data["menu_id"],
                text=menu_strings["text"].substitute(text=text),
                reply_markup=edit_text_keyboard
            )
    await state.set_state(None)
