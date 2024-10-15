from typing import List, Any

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from fastapi.params import Query
from starlette import status

from warehouse_management.dependency.check_permission import PermissionChecker
from warehouse_management.core.container import Container
from warehouse_management.dependency.product_depends import parse_product_query
from warehouse_management.enum.permission_enum import PermissionEnum
from warehouse_management.schema.base_schema import MessageResponseBase
from warehouse_management.schema.product_schema import ProductResponseSchema, FindProductSchema, ProductPublic, ProductBase, ProductAllDetailsPublic
from warehouse_management.services.product_service import ProductService

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.post(
    "",
    dependencies=[Depends(PermissionChecker([PermissionEnum.manage_product]))],
    status_code=status.HTTP_201_CREATED,
    response_model=ProductPublic,
    response_model_exclude_none=True,
    summary="Create product",
    description="Add new product to the stock",
)
@inject
async def create(
    info: ProductBase,
    service: ProductService = Depends(Provide[Container.product_service]),
) -> ProductPublic:
    return await service.add(info)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ProductResponseSchema,
    summary="Get All with param",
    description="Get with all products",
)
@inject
async def get_all_by_options(
        info: FindProductSchema = Depends(parse_product_query),
        service: ProductService = Depends(Provide[Container.product_service]),
) -> ProductResponseSchema:
    return await service.get_all_by_options(schema=info, with_count=True)


@router.get(
    "/by-ids",
    status_code=status.HTTP_200_OK,
    response_model=List[ProductPublic],
    summary="Get products by ids",
    description="Get list products by ids",
)
@inject
async def get_by_ids(
        ids: List[int] = Query(),
        service: ProductService = Depends(Provide[Container.product_service]),
) -> List[ProductPublic]:
    return await service.get_list_by_ids(ids)


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=ProductAllDetailsPublic,
    summary="Get product",
    description="Get product details by id",
)
@inject
async def get_one(
    id: int,
    service: ProductService = Depends(Provide[Container.product_service]),
) -> ProductAllDetailsPublic:
    return await service.get_by_id(id, True)


@router.put(
    "/{id}",
    dependencies=[Depends(PermissionChecker([PermissionEnum.manage_product]))],
    status_code=status.HTTP_200_OK,
    response_model=ProductPublic,
    response_model_exclude_none=True,
    summary="Edit product",
    description="Edit product details",
)
@inject
async def update(
    id: int,
    info: ProductBase,
    service: ProductService = Depends(Provide[Container.product_service]),
) -> ProductPublic:
    return await service.put_update(id, info)


@router.delete(
    "/delete-multi",
    dependencies=[Depends(PermissionChecker([PermissionEnum.manage_product]))],
    status_code=status.HTTP_200_OK,
    response_model=MessageResponseBase,
    response_model_exclude_none=True,
    summary="Delete multiple Products",
    description="Delete Products by ids",
)
@inject
async def delete_multi(
        ids: List[int] = Query(..., alias="ids"),
        service: ProductService = Depends(Provide[Container.product_service]),
) -> MessageResponseBase:
    await service.remove_multiple_by_ids(ids)
    return MessageResponseBase(message="Deleted successfully")


@router.delete(
    "/{id}",
    dependencies=[Depends(PermissionChecker([PermissionEnum.manage_product]))],
    status_code=status.HTTP_200_OK,
    response_model=MessageResponseBase,
    response_model_exclude_none=True,
    summary="Delete one Product",
    description="Delete Product by id",
)
@inject
async def delete(
        id: int,
        service: ProductService = Depends(Provide[Container.product_service])
) -> MessageResponseBase:
    await service.remove_by_id(id)
    return MessageResponseBase(message="Deleted successfully")
