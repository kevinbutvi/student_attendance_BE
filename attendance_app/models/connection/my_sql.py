

import os
import pymysql
from functools import wraps
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


load_dotenv()

MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASS = os.getenv('MYSQL_PASSWORD')
MYSQL_DB = os.getenv('MYSQL_DATABASE')
MYSQL_HOST = os.getenv('MYSQL_HOST')


engine = create_engine(
    f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASS}@{MYSQL_HOST}/{MYSQL_DB}')


def with_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Create a session factory
        Session = sessionmaker(bind=engine)
        # Create a session and call the function
        with Session() as session:
            result = func(session, *args, **kwargs)
        return result
    return wrapper
