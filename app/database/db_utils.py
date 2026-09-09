from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import MultipleResultsFound
from database import engine, User
from logging import error, info



class Utils:
    def __init__(self) -> None:
        self.email: str

    def get_token(self):
        with Session(engine) as session:
            result = session.execute(
                select(User).where(User.email == self.email)
            )
            
            try:
                user = result.scalar_one_or_none()
            except MultipleResultsFound:
                error(f"MultipleResultsFound for {self.email}")
                return None

            if user is None:
                return None

            info(f"Get token")
            return user.encrypt_token

    def set_token(self, encrypt_user_id: str, encrypt_new_token: str) -> None:
        with Session(engine) as session:
            result = session.execute(
                select(User).where(User.email == self.email)
            )

            try:
                user = result.scalar_one_or_none()
            except MultipleResultsFound:
                error(f"MultipleResultsFound for {self.email}")
                return

            if user:
                user.encrypt_token = encrypt_new_token
                info("Token update done")
            else:
                user = User(
                    email=self.email,
                    encrypt_user_id=encrypt_user_id,
                    encrypt_token=encrypt_new_token
                )
                session.add(user)
                info("New token write done")

            session.commit()