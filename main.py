from config import Config
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from pythonjsonlogger.json import JsonFormatter
import sys
from contextlib import asynccontextmanager
from baseservice.base_api import base_router

# Configure JSON logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(JsonFormatter())
handler.setLevel(logging.INFO)
logger.addHandler(handler)

config = Config()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    logger.info("Starting agents service...")
    app.state.db_path = config.db_path
    logger.info(f"database path set to: {app.state.db_path}")
    logger.info(f"service running on port: {config.port}")

    yield

    # shutdown
    logger.info("Shutting down service...")


app = FastAPI(
    title="agents service api",
    description="template service for building python projects",
    version="1.0.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:*", "http://127.0.0.1:*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(base_router, tags=["base_api"])


def main():
    logger.info("Hello from agents!", extra={"more_data": True})

    logger.info("Server configuration", extra={"port": config.port})
    uvicorn.run("main:app", host="0.0.0.0", port=int(config.port))


if __name__ == "__main__":
    main()
