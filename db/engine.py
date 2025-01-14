from sqlalchemy import create_engine

engine = create_engine("sqlite:///db/groupbot.db", echo=True)
