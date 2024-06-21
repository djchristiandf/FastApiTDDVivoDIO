from datetime import datetime
from typing import List
from uuid import UUID

import pymongo
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from store.db.mongo import db_client
from store.models.product import ProductModel
from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut
from store.core.exceptions import NotFoundException


class ProductUseCase:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient = db_client.get()
        self.database: AsyncIOMotorDatabase = self.client.get_database()
        self.collection = self.database.get_collection("products")

    async def create(self, body: ProductIn) -> ProductOut:
        product_model = ProductModel(**body.model_dump())
        result = await self.collection.insert_one(product_model.model_dump())

        if not result:
            raise NotFoundException(message="Product was not created.")

        return ProductOut(**product_model.model_dump())

    async def get(self, id: UUID) -> ProductOut:
        result = await self.collection.find_one({"id": id})

        if not result:
            raise NotFoundException(message="Product not find with value: {id}")

        return ProductOut(**result)

    async def get_by_price(
        self, min_price: float, max_price: float
    ) -> List[ProductOut]:
        filter_query = {"price": {"$gte": min_price, "$lte": max_price}}
        cursor = self.collection.find(filter_query)
        return [ProductOut(**item) async for item in cursor]

    async def query(self) -> List[ProductOut]:
        return [ProductOut(**item) async for item in self.collection.find()]

    async def update(self, id: UUID, body: ProductUpdate) -> ProductUpdateOut:
        result = await self.collection.find_one({"id": id})
        if not result:
            raise NotFoundException(message=f"Product with ID {id} not found")

        body_dict = body.model_dump()
        body_dict["updated_at"] = datetime.now()

        result = await self.collection.find_one_and_update(
            filter={"id": id},
            update={"$set": body.model_dump()},
            return_document=pymongo.ReturnDocument.AFTER,
        )

        return ProductUpdateOut(**result)

    async def delete(self, id: UUID) -> bool:
        result = await self.collection.find_one({"id": id})
        if not result:
            raise NotFoundException(message="Product not find with value: {id}")
        result = await self.collection.delete_one({"id": id})
        return True if result.deleted_count > 0 else False


product_usecase = ProductUseCase()
