from fastapi import HTTPException
from app.database import mongodb, mongodb_collection

from app.database import mongodb, mongodb_collection
from bson.objectid import ObjectId

class MongoDatabase:
  mongoDB = None
  mongoDB_collection = None

  @classmethod
  async def insert_into_db(cls, data):
    result = await cls.mongoDB_collection.insert_one(data)
    return str(result.inserted_id)

  @classmethod
  async def find_by_id(cls, id: str):
    try:
      document = await cls.mongoDB_collection.find_one({"_id": ObjectId(id)})
      return document
    except Exception as e:
      return {"error": str(e)}

  @classmethod
  async def find_by_filters(cls, **filters):
    cursor = cls.mongoDB_collection.find(filters)
    results = []
    async for document in cursor:
      results.append(document)
    return results


  @classmethod
  async def delete_by_id(cls, id: str):
    try:
      result = await cls.mongoDB_collection.delete_one({"_id": ObjectId(id)})
      if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Document not found")
      return {"message": "Document deleted successfully"}
    except Exception as e:
      raise HTTPException(status_code=400, detail=str(e))
