import os

from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseModel):

    TOKENTELEGRAM: str = os.getenv("TOKENTELEGRAM")
    CHAT_ID: str =os.getenv("CHAT_ID")
    DATABASE : str = os.getenv("DATABASE")
    IP_OYENTE: str = os.getenv("IP_OYENTE")

    DATABASEMYSQL: str = os.getenv('DATABASEMYSQL')
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM : str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES : int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

settings = Settings()   