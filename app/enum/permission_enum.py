from enum import Enum


class PermissionEnum(str, Enum):
    show_user = "show_user"
    manage_user = "manage_user"
    show_permission = "show_permission"
    manage_permission = "manage_permission"
    show_role = "show_role"
    manage_role = "manage_role"
    show_product = "show_product"
    manage_product = "manage_product"
    show_orders = "show_orders"
    show_order = "show_order"
    create_order = "create_order"
    manage_order = "manage_order"
    show_server_log = "show_server_log"
