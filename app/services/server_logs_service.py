from app.model import ServerLogsModel
from app.repository.server_logs_repository import ServerLogsRepository
from app.schema.server_logs_schema import ServerLogsUpsert, ServerLogsBase
from app.services.base_service import BaseService


class ServerLogsService(BaseService):
    def __init__(self, server_logs_repository: ServerLogsRepository):
        self.server_logs_repository = server_logs_repository
        super().__init__(server_logs_repository)

    # @staticmethod
    # def create_log_instance(schema: ServerLogsUpsert):
    #     return ServerLogsModel(**schema.model_dump())

    async def save_log(self, log: ServerLogsBase):
        if log.module:
            await self.server_logs_repository.create(log)
