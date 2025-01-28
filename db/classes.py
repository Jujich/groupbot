from sqlalchemy import ForeignKey, String, INT
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class Admin(Base):
    __tablename__ = "admins"
    id: Mapped[int] = mapped_column(INT, primary_key=True)
    tgId: Mapped[int] = mapped_column(INT, unique=True)
    username: Mapped[str] = mapped_column(String)
    join_date: Mapped[str] = mapped_column(String)
    default_text: Mapped[str] = mapped_column(String)
    date: Mapped[str] = mapped_column(String)
    time: Mapped[str] = mapped_column(String)

    def __repr__(self) -> str:
        return f"Admin(id={self.id!r}, tgId={self.tgId!r}, username={self.username!r}, join_date={self.join_date!r}, default_text={self.default_text!r}, date={self.date!r}, time={self.time!r})"


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(INT, primary_key=True)
    tgId: Mapped[int] = mapped_column(INT, unique=True)
    username: Mapped[str] = mapped_column(String)
    join_date: Mapped[str] = mapped_column(String)
    subscribed_channels: Mapped[str] = mapped_column(String)

    def __repr__(self) -> str:
        return (f"User(id={self.id}, tgId={self.tgId}, username={self.username}, join_date={self.join_date}, "
                f"subscribed_channels={self.subscribed_channels})")


class Channel(Base):
    __tablename__ = "channels"
    id: Mapped[int] = mapped_column(INT, primary_key=True)
    tgChannelId: Mapped[int] = mapped_column(INT, unique=True)
    title: Mapped[str] = mapped_column(String)
    admin_tgid: Mapped[int] = mapped_column(INT, ForeignKey(Admin.tgId))
    text: Mapped[str] = mapped_column(String)
    schedule: Mapped[str] = mapped_column(String)

    def __repr__(self) -> str:
        return f"Channel(id={self.id}, tgChannelId={self.tgChannelId}, title={self.title}, admin_tgid={self.admin_tgid})"
