from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine("sqlite+aiosqlite:///storage/vidpro.db", echo=True, poolclass=StaticPool)