from typing import List

from warehouse_management.repository.product_repository import ProductRepository
from warehouse_management.schema.product_schema import FindProductSchema
from warehouse_management.services.base_service import BaseService


class ProductService(BaseService):
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
        super().__init__(product_repository)

    async def get_list_by_ids(self, ids: List[int], get_eager: bool = False):
        finder = FindProductSchema()
        finder.id__in = ids
        return await self.get_all_by_options(finder, get_eager)
