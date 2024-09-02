import asyncio
from app.database import engine
from app.models import Base

async def init_db():
    # Begin an asynchronous connection to the database
    async with engine.begin() as conn:
        # Run the SQL command to create all tables defined in the models
        await conn.run_sync(Base.metadata.create_all)

# Check if the script is being run directly
if __name__ == "__main__":
    # Run the init_db function asynchronously
    asyncio.run(init_db())


