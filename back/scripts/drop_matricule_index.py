"""
Script to drop the matricule index from the users collection.
Run this once after removing matricule from the codebase.
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings


async def drop_matricule_index():
    """Drop the matricule unique index from users collection."""
    client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)
    db = client[settings.MONGO_DB_NAME]
    users_collection = db["users"]
    
    try:
        # List all indexes
        indexes = await users_collection.index_information()
        print("Current indexes:", indexes.keys())
        
        # Drop the matricule index if it exists
        for index_name, index_info in indexes.items():
            if 'matricule' in str(index_info.get('key', [])):
                print(f"Dropping index: {index_name}")
                await users_collection.drop_index(index_name)
                print(f"✅ Successfully dropped index: {index_name}")
        
        # List indexes again to confirm
        indexes_after = await users_collection.index_information()
        print("\nIndexes after cleanup:", indexes_after.keys())
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        client.close()


if __name__ == "__main__":
    asyncio.run(drop_matricule_index())
