import logging
from contextlib import asynccontextmanager

from dependency_injector.wiring import inject
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from app.core.config import configs
from app.core.container import Container
from app.core.exception_handlers import (
    http_exception_handler,
    req_validation_exception_handler,
    res_validation_exception_handler,
)
from app.dependency.request_control_middleware import RequestControlMiddleware
from app.util.class_object import singleton

from app.api.v1.routes import routers as v1_routers
from app.core.log_config import configure_logging

logger = logging.getLogger(__name__)


@singleton
class AppCreator:
    def __init__(self):
        # set app default
        self.app = FastAPI(
            title=configs.PROJECT_NAME,
            openapi_url=f"{configs.API}/openapi.json",
            version="2.0.0",
            lifespan=self.lifespan,
        )

        # set db and container
        self.container = Container()
        self.container.init_resources()
        self.container.wire(modules=[__name__])

        self.db = self.container.db()

        # set cors:
        if configs.BACKEND_CORS_ORIGINS:
            self.app.add_middleware(
                CORSMiddleware,
                allow_origins=[origin for origin in configs.BACKEND_CORS_ORIGINS],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )

        # Add Middleware
        self.app.add_middleware(RequestControlMiddleware)

        # Handle exceptions:
        self.app.add_exception_handler(HTTPException, http_exception_handler)
        self.app.add_exception_handler(RequestValidationError, req_validation_exception_handler)
        self.app.add_exception_handler(ResponseValidationError, res_validation_exception_handler)

        # set routers:
        @self.app.get("/")
        def root():
            return "Service is working"

        self.app.include_router(v1_routers, prefix=configs.API_V1_STR)

    @asynccontextmanager
    @inject
    async def lifespan(self, app: FastAPI):
        # Startup
        configure_logging()
        logger.info("Starting main app")

        yield

        # Shutdown
        logger.info("Stopped main app")

app_creator = AppCreator()
app = app_creator.app
db = app_creator.db
container = app_creator.container
