from typing import List

from app.repository.order_repository import OrderRepository
from app.schema.base_schema import MessageResponseBase
from app.schema.order_schema import FindOrderSchema, OrderCreateSchema, OrderBase
from app.services.base_service import BaseService


class OrderService(BaseService):
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository
        super().__init__(order_repository)

    async def add_order(self, order_data: OrderBase, username: str):
        order = OrderCreateSchema(**order_data.model_dump(), username=username)
        await self.order_repository.create_order(order)
        return MessageResponseBase(message="Order added successfully")

    async def get_list_by_ids(self, ids: List[int], get_eager: bool = False):
        finder = FindOrderSchema()
        finder.id__in = ids
        return await self.get_all_by_options(finder, get_eager)

    async def get_my_orders(self, username: str):
        finder = FindOrderSchema()
        finder.username = username
        return await self.get_all_by_options(finder, get_eager=False)

    async def get_my_order(self, order_id: int, username: str):
        finder = FindOrderSchema()
        finder.id = order_id
        finder.username = username
        return await self.get_one_by_options(finder, get_eager=True, not_found_error=True)
