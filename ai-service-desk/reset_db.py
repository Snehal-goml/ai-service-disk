import asyncio
from app.core.database import engine, Base
from sqlalchemy import text

async def main():
    async with engine.connect() as conn:
        await conn.execute(text("DROP TABLE IF EXISTS tickets CASCADE"))
        await conn.commit()
        print("Dropped tickets table")
    
    # Create all tables with new schema
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("Created tickets table with new schema (integer ID)")

if __name__ == "__main__":
    asyncio.run(main())