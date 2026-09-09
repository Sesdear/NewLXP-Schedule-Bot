from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import os
import logging

DB_HOST = os.getenv("DB_HOST")
if DB_HOST is None:
    logging.error("DB_HOST Env variable not configured!")
    exit(1)
    
engine = create_engine(DB_HOST)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    encrypt_password: Mapped[str] = mapped_column(nullable=False, unique=False)
    encypt_user_id: Mapped[str] = mapped_column(nullable=False, unique=True)
    encrypt_token: Mapped[str] = mapped_column(nullable=False)
    
Base.metadata.create_all(engine)

