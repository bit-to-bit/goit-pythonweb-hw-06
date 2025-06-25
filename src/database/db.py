"""DB config"""

import configparser

import pathlib
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


def get_db_url() -> str:
    """DB connection string"""
    file_config = pathlib.Path(__file__).parent.parent.parent.joinpath("config.ini")
    config = configparser.ConfigParser()
    config.read(file_config)

    username = config.get("DB", "user")
    password = config.get("DB", "password")
    domain = config.get("DB", "domain")
    port = config.get("DB", "port")
    db_name = config.get("DB", "db_name")

    return f"postgresql://{username}:{password}@{domain}:{port}/{db_name}"


engine = create_engine(get_db_url(), echo=False)
DBSession = sessionmaker(bind=engine)
session = DBSession()
