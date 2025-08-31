from fastapi import APIRouter, Depends, Request, HTTPException
from repository.database import SQLite3Database
from .base_service import BaseService
from config import Config

base_router = APIRouter()


def get_db_conn(request: Request):
    db_path = request.app.state.db_path
    db = SQLite3Database(db_path=db_path)
    with db.get_connection() as conn:
        yield conn


def get_base_service(request: Request, conn=Depends(get_db_conn)):
    config = Config()
    return BaseService(conn, config)


@base_router.get("/")
async def home(baseservice: BaseService = Depends(get_base_service)) -> dict:
    try:
        return baseservice.test()
    except Exception:
        raise HTTPException(status_code=404, detail="prompt not found")


@base_router.get("/health")
async def health_check() -> dict:
    """Health check endpoint"""
    return {"status": "healthy", "service": "agents"}


@base_router.get("/user/{username}")
async def get_user(
    username: str,
    baseservice: BaseService = Depends(get_base_service),
):
    return baseservice.get_user(username)
