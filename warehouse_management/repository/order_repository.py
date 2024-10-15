from contextlib import AbstractAsyncContextManager
from typing import Callable, List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from warehouse_management.core.exceptions import InternalError, NotFoundError
from warehouse_management.model import OrderModel, ProductModel, OrderItemModel
from warehouse_management.repository.base_repository import BaseRepository
from warehouse_management.repository.product_repository import ProductRepository
from warehouse_management.schema.order_item_schema import OrderItemSchema
from warehouse_management.schema.order_schema import OrderCreateSchema
from warehouse_management.schema.product_schema import FindProductSchema, ProductPublic


class OrderRepository(BaseRepository):
    def __init__(
            self,
            async_session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]],
            product_repository: ProductRepository,
    ) -> None:
        self.async_session_factory = async_session_factory
        self.product_repository = product_repository
        super().__init__(async_session_factory, OrderModel)

    async def create_order(self, data: OrderCreateSchema):
        products, items_dict = await self.check_quantity_stock(data.products)
        async with self.async_session_factory() as async_session:
            try:
                new_order = OrderModel(
                    delivery_address=data.delivery_address,
                    status=data.status,
                    username=data.username,
                )
                async_session.add(new_order)

                for item in products:
                    order_item = OrderItemModel(
                        order=new_order,
                        product=item,
                        quantity=items_dict[f'{item.id}']
                    )
                    async_session.add(order_item)
                    item.quantity_in_stock -= items_dict[f'{item.id}']
                    await async_session.merge(item)
                await async_session.commit()
            except Exception as error:
                raise InternalError(detail=str(f"OrderRepository->create_order: {error}"))

    async def check_quantity_stock(self, items: List[OrderItemSchema]) -> tuple[List[ProductPublic], dict]:
        finder = FindProductSchema()
        finder.id__in = []
        items_dict = {}
        msg = ""
        for item in items:
            if f"{item.product_id}" in items_dict:
                items_dict[f"{item.product_id}"] += item.quantity
            else:
                finder.id__in.append(item.product_id)
                items_dict[f"{item.product_id}"] = item.quantity
        products: List[ProductModel] = await self.product_repository.read_all_by_options(finder)
        if not len(products) or len(products) != len(items_dict):
            raise NotFoundError(detail="Not found all products from database")
        for product in products:
            if (product.quantity_in_stock - items_dict[f"{product.id}"]) < 0:
                msg += f"{product.title} = Available quantity: {product.quantity_in_stock}, Requested quantity: {items_dict[f'{product.id}']}\n "
        if len(msg):
            raise HTTPException(
                status_code=400,
                detail=msg
            )
        return products, items_dict
