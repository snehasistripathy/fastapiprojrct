from contextlib import asynccontextmanager

from app.schemas.student import CICDTestRequest
from fastapi import FastAPI

from app.core.config import (
    APP_NAME,
    DEBUG,
    API_V1_PREFIX
)

from app.core.logging import (
    setup_logging,
    logger
)

from app.api.v1.router import router as api_router

# Register models with SQLAlchemy metadata
from app.models import Student


setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("Student Management API starting")

    yield

    logger.info("Student Management API shutting down")


app = FastAPI(
    title=APP_NAME,
    description="Student Management System",
    version="1.0.0",
    debug=DEBUG,
    lifespan=lifespan
)


app.include_router(
    api_router,
    prefix=API_V1_PREFIX
)


@app.get("/")
def root():

    return {
        "message": "Welcome to Student Management API",
        "status": "running"
    }
@app.post("/cicd-test")
async def cicd_test(data: CICDTestRequest):

    return {
        "message": "CI/CD deployment successful!",
        "received_data": {
            "message": data.message,
            "version": data.version
        },
        "status": "success"
    }


@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }