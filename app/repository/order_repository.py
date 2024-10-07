from contextlib import AbstractAsyncContextManager
from typing import Callable, List

from sqlalchemy.ext.asyncio import AsyncSession

from app.model import OrderModel, ProductModel, OrderItemModel
from app.repository.base_repository import BaseRepository
from app.schema.order_schema import OrderCreateSchema


class OrderRepository(BaseRepository):
    def __init__(
            self,
            async_session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]],
    ) -> None:
        self.async_session_factory = async_session_factory
        super().__init__(async_session_factory, OrderModel)

    async def create_order(self, data: OrderCreateSchema):
        async with self.async_session_factory() as async_session:
            try:
                new_order = OrderModel(
                    delivery_address=data.delivery_address,
                    status=data.status,
                    username=data.username,
                )
                async_session.add(new_order)

                for item in data.products:
                    product = await async_session.get(ProductModel, item.product_id)

                    if product:
                        order_item = OrderItemModel(
                            order=new_order,
                            product=product,
                            quantity=item.quantity
                        )
                        async_session.add(order_item)

                await async_session.commit()
            except Exception as error:
                raise error
