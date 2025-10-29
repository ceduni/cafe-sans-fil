"""
Migration script to remove matricule field from all existing user documents.
This is optional but recommended for database cleanup.
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings


async def remove_matricule_field():
    """Remove matricule field from all user documents."""
    client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)
    db = client[settings.MONGO_DB_NAME]
    users_collection = db["users"]
    
    try:
        # Count users with matricule field
        count = await users_collection.count_documents({"matricule": {"$exists": True}})
        print(f"Found {count} users with matricule field")
        
        if count == 0:
            print("✅ No users have matricule field. Nothing to migrate.")
            return
        
        # Remove matricule field from all documents
        result = await users_collection.update_many(
            {"matricule": {"$exists": True}},
            {"$unset": {"matricule": ""}}
        )
        
        print(f"✅ Successfully removed matricule from {result.modified_count} users")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        client.close()


if __name__ == "__main__":
    asyncio.run(remove_matricule_field())
