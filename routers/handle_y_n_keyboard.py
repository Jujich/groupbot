from bot import bot
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from strings.menu_strings import menu_strings
from strings.message_strings import message_strings
from keyboards.prebuilt import (edit_text_keyboard,
                                edit_default_text_keyboard,
                                edit_schedule_keyboard,
                                start_keyboard,
                                edit_amount_keyboard)
from db.db_requests import (update_group_text,
                            update_default_text,
                            get_channels_by_admin_id,
                            update_schedule_time,
                            update_schedule_date,
                            update_group_amount,
                            get_group_schedule,
                            delete_last_group_amount)
from string import Template
from routers.handle_schedule.handle_schedule import calculate_price
from routers.menu.group_data.get_amount import prepare_group_schedule
import logging

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
            group_data = get_group_schedule(state_data["channel_id"])
            price = await calculate_price(int(group_data["amount"]))
            text = text.substitute(price=price, amount=group_data[0])
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
        elif state_state == "enter_amount":
            if update_group_amount(state_data["channel_id"], state_data["amount"]):
                await call.answer(
                    show_alert=True,
                    text=menu_strings["edit_text_success"]
                )
            else:
                await call.answer(
                    show_alert=True,
                    text=menu_strings["edit_text_failure"]
                )
            group_data = get_group_schedule(state_data["channel_id"])
            res_schedule = await prepare_group_schedule(group_data, call.from_user.id)
            await bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=state_data["menu_id"],
                text=menu_strings["get_amount"].substitute(schedule=res_schedule),
                reply_markup=edit_amount_keyboard
            )
        elif state_state == "groups_send_messages":
            groups = await get_channels_by_admin_id(call.from_user.id)
            text = state_data["text"]
            for group in groups:
                try:
                    await bot.send_message(
                        chat_id=group.tgChannelId,
                        text=text
                    )
                except Exception as e:
                    await bot.send_message(
                        chat_id=call.from_user.id,
                        text=menu_strings["groups_send_messages_failure"].substitute(group=group.title)
                    )
                    logging.exception(e)
            await call.answer(
                show_alert=True,
                text=menu_strings["groups_send_messages_success"]
            )

            await bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=state_data["menu_id"],
                text=message_strings["start"],
                reply_markup=start_keyboard
            )
        elif state_state == "delete_amount":
            if delete_last_group_amount(state_data["channel_id"]):
                await call.answer(
                    show_alert=True,
                    text=menu_strings["edit_text_success"]
                )
            else:
                await call.answer(
                    show_alert=True,
                    text=menu_strings["edit_text_failure"]
                )
            group_data = get_group_schedule(state_data["channel_id"])
            res_schedule = await prepare_group_schedule(group_data, call.from_user.id)
            await bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=state_data["menu_id"],
                text=menu_strings["get_amount"].substitute(schedule=res_schedule),
                reply_markup=edit_amount_keyboard
            )
    await state.set_state(None)
