from warehouse_management.repository.server_logs_repository import ServerLogsRepository
from warehouse_management.schema.server_logs_schema import ServerLogsBase
from warehouse_management.services.base_service import BaseService


class ServerLogsService(BaseService):
    def __init__(self, server_logs_repository: ServerLogsRepository):
        self.server_logs_repository = server_logs_repository
        super().__init__(server_logs_repository)

    async def save_log(self, log: ServerLogsBase):
        if log.module:
            await self.server_logs_repository.create(log)
