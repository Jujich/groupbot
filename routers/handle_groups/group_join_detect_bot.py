from aiogram.types import ChatMemberUpdated
from bot import bot
from aiogram import Router
from db.db_requests import insert_channel, delete_channel, get_admin_by_chat_id
from strings.group_strings import group_strings
from strings.menu_strings import menu_strings
from keyboards.prebuilt import delete_message_keyboard

router = Router()


@router.my_chat_member()
async def handle_group_join_bot(update: ChatMemberUpdated):
    if update.new_chat_member.user.id == bot.id:
        if update.new_chat_member.status == 'administrator':
            admins = await bot.get_chat_administrators(update.chat.id)

            owner_id = None
            for admin in admins:
                if admin.status == "creator":
                    owner_id = admin.user.id

            if owner_id is not None:
                data = {
                    "tgChannelId": update.chat.id,
                    "title": update.chat.title,
                    "adminTgId": owner_id,
                }
                if insert_channel(data):
                    await bot.send_message(
                        text=group_strings["add_group"].substitute(group=data['title'],),
                        chat_id=data['adminTgId'],
                        reply_markup=delete_message_keyboard
                    )
                else:
                    await bot.send_message(
                        text=group_strings["error_database"],
                        chat_id=data['tgChannelId'],
                    )
                    await bot.leave_chat(update.chat.id)
            else:
                await bot.send_message(chat_id=update.chat.id, text=group_strings["error_owner_not_found"])
                await bot.leave_chat(update.chat.id)
        elif update.new_chat_member.status == 'left' or update.new_chat_member.status == 'kicked':
            try:
                admin_id = get_admin_by_chat_id(update.chat.id)
                await bot.send_message(
                    chat_id=admin_id,
                    text=menu_strings["left_group"].substitute(title=update.chat.title),
                    reply_markup=delete_message_keyboard,
                )
                delete_channel(update.chat.id)
            except AttributeError:
                pass
