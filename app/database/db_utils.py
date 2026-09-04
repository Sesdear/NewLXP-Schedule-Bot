from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import MultipleResultsFound
from database import engine, Newlxp
from logging import error, info



class Utils:
    def __init__(self) -> None:
        self.email: str

    def get_token(self):
        with Session(engine) as session:
            result = session.execute(
                select(Newlxp).where(Newlxp.email == self.email)
            )
            
            try:
                user = result.scalar_one_or_none()
            except MultipleResultsFound:
                error(f"MultipleResultsFound for {self.email}")
                return None

            if user is None:
                return None

            info(f"Get token")
            return user.token

    def set_token(self, user_id: str, new_token: str) -> None:
        with Session(engine) as session:
            result = session.execute(
                select(Newlxp).where(Newlxp.email == self.email)
            )

            try:
                user = result.scalar_one_or_none()
            except MultipleResultsFound:
                error(f"MultipleResultsFound for {self.email}")
                return

            if user:
                user.token = new_token
                info("Token update done")
            else:
                user = Newlxp(
                    email=self.email,
                    user_id=user_id,
                    token=new_token
                )
                session.add(user)
                info("New token write done")

            session.commit()