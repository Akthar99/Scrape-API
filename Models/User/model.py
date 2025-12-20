from __future__ import annotations
from sqlalchemy import ForeignKey, func, Column, select
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime
import asyncio


from config import DATABASE_URL

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    fullname: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    user_email: Mapped[str] = mapped_column(nullable=False)
    api_key: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    card: Mapped[str]

class Subscription(Base):
    __tablename__ = "subscription"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    subscription_plan: Mapped[str] = mapped_column(nullable=False)
    request: Mapped[int] = mapped_column(default=0)
    monthly_bill: Mapped[int] = mapped_column(nullable=False)

class CardInformation(Base):
    __tablename__ = "card_information"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    card_name: Mapped[str] = mapped_column(nullable=False)
    card_number: Mapped[str] = mapped_column(nullable=False)
    expiry_month: Mapped[str] = mapped_column(nullable=False)
    expiry_year: Mapped[str] = mapped_column(nullable=False)
    card_cvv: Mapped[str] = mapped_column(nullable=False)
    card_type: Mapped[str] = mapped_column(nullable=False)

async def async_main():
    engine = create_async_engine(DATABASE_URL, echo=True)
    
    async_session = async_sessionmaker(engine, expire_on_commit=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()

async def init_db():
    await async_main()

def get_engine():
    return create_async_engine(DATABASE_URL, echo=True)

def get_async_session(engine: AsyncEngine):
    return async_sessionmaker(engine, expire_on_commit=False)

async def get_subscription_plan(api_key: str, async_session: async_sessionmaker[AsyncSession]) -> str | None:
    """
    Retrieve the subscription plan for a user based on their API key.
    @param api_key: The API key of the user.
    @param session: The asynchronous database session.
    @return: The subscription plan as a string, or None if not found.
    """
    async with async_session() as session:
        result = await session.execute(
            select(Subscription.subscription_plan).join(User).where(User.api_key == api_key)
        )
        return result.scalars().first()

async def authenticate_api_key(api_key: str, async_session: async_sessionmaker[AsyncSession]) -> bool:
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.api_key == api_key)
        )
        user = result.scalars().first()
        return True if user is not None else False



# asyncio.run(async_main())