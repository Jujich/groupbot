import json
from aiogram.exceptions import TelegramForbiddenError
from aiogram.methods import GetChatMember
from aiogram.types import ChatMember
from bot import bot
from db.engine import engine
from db.classes import Admin, User, Channel
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime
from strings.menu_strings import menu_strings
from string import Template


def insert_admin(data: dict) -> bool:
    session = Session(engine)
    try:
        admin = Admin(
            username="@" + data["username"],
            tgId=data["tgId"],
            join_date=str(datetime.now()).split('.')[0],
            default_text=menu_strings["default_text"],
            date=menu_strings["default_date"],
            time=menu_strings["default_time"],
        )
        session.add(admin)
        session.commit()
        session.close()
        return True
    except:
        session.close()
        return False


def insert_user(data: dict) -> bool:
    session = Session(engine)
    try:
        user = User(
            username="@" + data["username"],
            tgId=data["tgId"],
            join_date=str(datetime.now()).split('.')[0],
            subscribed_channels=json.dumps(data["subscribed_channels"]),
        )
        session.add(user)
        session.commit()
        session.close()
        return True
    except:
        session.close()
        return False


def user_check_in_db(tgId: int) -> User:
    session = Session(engine)
    stmt = select(User).where(User.tgId == tgId)
    user = session.scalars(stmt).first()
    session.close()
    return user


def user_get_subscribed_channels(tgId: int) -> list:
    session = Session(engine)
    user = session.query(User).filter(User.tgId == tgId).first()
    session.close()
    return user.subscribed_channels


def user_update_subscribed_channels(tgId: int, channel_id: int) -> bool:
    session = Session(engine)
    try:
        user = session.query(User).filter(User.tgId == tgId).first()
        channels = json.loads(user.subscribed_channels)
        channels.append(channel_id)
        user.subscribed_channels = json.dumps(channels)
        session.commit()
        session.close()
        return True
    except:
        session.close()
        return False


def user_remove_subscribed_channel(tgId: int, channel_id: int) -> bool:
    session = Session(engine)
    try:
        user = session.query(User).filter(User.tgId == tgId).first()
        channels = json.loads(user.subscribed_channels)
        channels.remove(channel_id)
        user.subscribed_channels = json.dumps(channels)
        session.commit()
        session.close()
        return True
    except:
        session.close()
        return False


def delete_user(tgId: int, channel_id: int) -> bool:
    session = Session(engine)
    try:
        user = session.query(User).filter(User.tgId == tgId).first()

        if user:
            session.delete(user)
            session.commit()
            session.close()
            return True
        else:
            return False
    except Exception as e:
        print(e)
        session.close()
        return False


async def get_channels_by_admin_id(admin_id: int) -> list:
    session = Session(engine)
    stmt = select(Channel).where(Channel.admin_tgid == admin_id)
    channels = []
    for channel in session.scalars(stmt):
        channels.append(channel)
    session.close()
    return channels


def insert_channel(data: dict) -> bool:
    session = Session(engine)
    try:
        channel = Channel(
            tgChannelId=data["tgChannelId"],
            title=data["title"],
            admin_tgid=data["adminTgId"],
            text=get_default_text(int(data["adminTgId"])),
            price=menu_strings["default_price"],
            amount=menu_strings["default_amount"],
        )
        session.add(channel)
        session.commit()
        session.close()
        return True
    except:
        session.close()
        return False


def delete_channel(channel_id: int) -> bool:
    session = Session(engine)
    try:
        channel = session.query(Channel).filter(Channel.tgChannelId == channel_id).first()

        if channel:
            session.delete(channel)
            session.commit()
            session.close()
            return True
        else:
            return False
    except Exception as e:
        print(e)
        session.close()
        return False


def get_all_channels() -> list[Channel]:
    session = Session(engine)
    stmt = select(Channel)
    channels = []
    for channel in session.scalars(stmt):
        channels.append(channel)
    session.close()
    return channels


async def get_all_admins() -> list[Admin]:
    session = Session(engine)
    stmt = select(Admin)
    admins = []
    for admin in session.scalars(stmt):
        admins.append(admin)
    session.close()
    return admins


async def clear_left_channels() -> None:
    channels = get_all_channels()
    for channel in channels:
        try:
            chat_member: ChatMember = await bot(GetChatMember(chat_id=channel.tgChannelId, user_id=bot.id))
            if chat_member.status in ['member', 'administrator']:
                pass
            else:
                delete_channel(channel.tgChannelId)
        except TelegramForbiddenError as e:
            delete_channel(channel.tgChannelId)


def get_admin_by_chat_id(channel_id: int) -> int:
    session = Session(engine)
    channel = session.query(Channel).filter(Channel.tgChannelId == channel_id).first()
    admin_id = channel.admin_tgid
    session.close()
    return admin_id


def get_user_schedule(admin_id: int) -> dict:
    session = Session(engine)
    admin = session.query(Admin).filter(Admin.tgId == admin_id).first()
    session.close()
    return {"date": admin.date, "time": admin.time}


def get_group_text(channel_id: int) -> Template:
    session = Session(engine)
    channel = session.query(Channel).filter(Channel.tgChannelId == channel_id).first()
    session.close()
    return Template(channel.text)


def get_group_data(channel_id: int) -> dict:
    session = Session(engine)
    channel = session.query(Channel).filter(Channel.tgChannelId == channel_id).first()
    session.close()
    return {"price": channel.price, "amount": channel.amount}


def update_schedule_time(admin_id: int, time: str) -> bool:
    session = Session(engine)
    try:
        admin = session.query(Admin).filter(Admin.tgId == admin_id).first()
        admin.time = time
        session.commit()
        session.close()
        return True
    except:
        session.close()
        return False


def update_schedule_date(admin_id: int, date: str) -> bool:
    session = Session(engine)
    try:
        admin = session.query(Admin).filter(Admin.tgId == admin_id).first()
        admin.date = date
        session.commit()
        session.close()
        return True
    except:
        session.close()
        return False


def update_group_text(channel_id: int, text: str) -> bool:
    session = Session(engine)
    try:
        channel = session.query(Channel).filter(Channel.tgChannelId == channel_id).first()
        channel.text = text
        session.commit()
        session.close()
        return True
    except:
        session.close()
        return False


def get_group_name(group_id: int) -> str:
    session = Session(engine)
    channel = session.query(Channel).filter(Channel.tgChannelId == group_id).first()
    session.close()
    return channel.title


def get_default_text(admin_id: int) -> str:
    session = Session(engine)
    admin = session.query(Admin).filter(Admin.tgId == admin_id).first()
    session.close()
    return admin.default_text


def update_default_text(admin_id: int, text: str) -> bool:
    session = Session(engine)
    try:
        admin = session.query(Admin).filter(Admin.tgId == admin_id).first()
        admin.default_text = text
        session.commit()
        session.close()
        return True
    except:
        session.close()
        return False


def update_group_price(channel_id: int, price: str) -> bool:
    session = Session(engine)
    try:
        channel = session.query(Channel).filter(Channel.tgChannelId == channel_id).first()
        channel.price = price
        session.commit()
        session.close()
        return True
    except:
        session.close()
        return False


def update_group_amount(channel_id: int, amount: str) -> bool:
    session = Session(engine)
    try:
        channel = session.query(Channel).filter(Channel.tgChannelId == channel_id).first()
        channel.amount = amount
        session.commit()
        session.close()
        return True
    except:
        session.close()
        return False
