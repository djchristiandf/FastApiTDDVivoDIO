from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from store.db.mongo import db_client


class ProductUseCase:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient = db_client.get()
        self.databse: AsyncIOMotorDatabase = self.client.get_database()
        self.collection = self.databse.get_collection("products")


product_usecase = ProductUseCase()
