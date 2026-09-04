from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine = create_engine("sqlite:////data/user.db")

class Base(DeclarativeBase):
    pass

class Newlxp(Base):
    __tablename__ = "newlxp"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    user_id: Mapped[str] = mapped_column(nullable=False, unique=True)
    token: Mapped[str] = mapped_column(nullable=False)
    
Base.metadata.create_all(engine)

