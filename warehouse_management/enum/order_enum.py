from enum import Enum


class OrderStatusEnum(str, Enum):
    in_process = "in_process"
    sent = "sent"
    delivered = "delivered"
