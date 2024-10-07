from typing import List

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from fastapi.params import Query
from starlette import status

from app.dependency.check_permission import PermissionChecker
from app.core.container import Container
from app.dependency.order_depends import parse_order_query
from app.dependency.token import JWTBearer
from app.dependency.user_token import get_current_user_payload
from app.enum.permission_enum import PermissionEnum
from app.schema.auth_schema import PayloadSchema
from app.schema.base_schema import MessageResponseBase
from app.schema.order_schema import FindOrderSchema, OrderResponseSchema, OrderPublic, OrderPublicWithProducts, OrderCreate, \
    OrderPublicWithProductsAndUser
from app.services.order_service import OrderService

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
    # dependencies=[Depends(JWTBearer())]
)


@router.post(
    "",
    dependencies=[Depends(PermissionChecker([PermissionEnum.create_order]))],
    status_code=status.HTTP_200_OK,
    response_model=MessageResponseBase,
    response_model_exclude_none=True,
    summary="Create product",
    description="Add new product to the stock",
)
@inject
async def create(
    info: OrderCreate,
    current_user: PayloadSchema = Depends(get_current_user_payload),
    service: OrderService = Depends(Provide[Container.order_service]),
) -> MessageResponseBase:
    return await service.add_order(info, current_user.username)


@router.get(
    "",
    dependencies=[Depends(PermissionChecker([PermissionEnum.show_orders]))],
    status_code=status.HTTP_200_OK,
    response_model=OrderResponseSchema,
    summary="Get Orders",
    description="Get All Orders",
)
@inject
async def get_all_by_options(
        info: FindOrderSchema = Depends(parse_order_query),
        service: OrderService = Depends(Provide[Container.order_service]),
) -> OrderResponseSchema:
    return await service.get_all_by_options(schema=info, get_eager=False, with_count=True)


@router.get(
    "/by-ids",
    dependencies=[Depends(PermissionChecker([PermissionEnum.show_orders]))],
    status_code=status.HTTP_200_OK,
    response_model=List[OrderPublic],
    summary="Get Orders by ids",
    description="Get list of Orders by ids",
)
@inject
async def get_by_ids(
        ids: List[int] = Query(),
        service: OrderService = Depends(Provide[Container.order_service]),
) -> List[OrderPublic]:
    return await service.get_list_by_ids(ids)


@router.get(
    "/my-orders",
    dependencies=[Depends(PermissionChecker([PermissionEnum.show_order]))],
    status_code=status.HTTP_200_OK,
    response_model=List[OrderPublic],
    summary="Get Orders by user token",
    description="Get list of Orders by user token",
)
@inject
async def get_by_user_token(
        service: OrderService = Depends(Provide[Container.order_service]),
        current_user: PayloadSchema = Depends(get_current_user_payload),
) -> List[OrderPublic]:
    return await service.get_my_orders(current_user.username)


@router.get(
    "/my-orders/{order_id}",
    dependencies=[Depends(PermissionChecker([PermissionEnum.show_order]))],
    status_code=status.HTTP_200_OK,
    response_model=OrderPublicWithProducts,
    summary="Get Orders by user token",
    description="Get list of Orders by user token",
)
@inject
async def get_by_user_token(
        order_id: int,
        service: OrderService = Depends(Provide[Container.order_service]),
        current_user: PayloadSchema = Depends(get_current_user_payload),
) -> OrderPublicWithProducts:
    return await service.get_my_order(order_id, current_user.username)


@router.get(
    "/{id}",
    dependencies=[Depends(PermissionChecker([PermissionEnum.show_orders]))],
    status_code=status.HTTP_200_OK,
    response_model=OrderPublicWithProductsAndUser,
    summary="Get order",
    description="Get order details by id",
)
@inject
async def get_one(
    id: int,
    service: OrderService = Depends(Provide[Container.order_service]),
) -> OrderPublicWithProductsAndUser:
    return await service.get_by_id(id, get_eager=True)


@router.delete(
    "/multi",
    dependencies=[Depends(PermissionChecker([PermissionEnum.manage_order]))],
    status_code=status.HTTP_200_OK,
    response_model=MessageResponseBase,
    response_model_exclude_none=True,
    summary="Delete multiple Orders",
    description="Delete multiple Orders by ids",
)
@inject
async def delete_multi(
        ids: List[int] = Query(..., alias="ids"),
        service: OrderService = Depends(Provide[Container.order_service]),
) -> MessageResponseBase:
    await service.remove_multiple_by_ids(ids)
    return MessageResponseBase(message="Deleted successfully")


@router.delete(
    "/{id}",
    dependencies=[Depends(PermissionChecker([PermissionEnum.manage_order]))],
    status_code=status.HTTP_200_OK,
    response_model=MessageResponseBase,
    response_model_exclude_none=True,
    summary="Delete one Order",
    description="Delete Order by id",
)
@inject
async def delete(
        id: int, service: OrderService = Depends(Provide[Container.order_service])
) -> MessageResponseBase:
    await service.remove_by_id(id)
    return MessageResponseBase(message="Deleted successfully")
