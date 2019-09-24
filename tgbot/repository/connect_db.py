from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def engine():
    connect = create_engine('postgresql://postgres:fender@localhost:5432/tgbot')
    return connect


Session = sessionmaker(bind=engine())

Base = declarative_base()
