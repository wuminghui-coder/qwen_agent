from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
from fastapi import APIRouter
from fastapi import FastAPI, HTTPException, Depends, Header

import logging
logger = logging.getLogger(__name__)

login_router = APIRouter()
async def authenticate(api_key: str = Header(..., alias="Authorization")):
    #raise HTTPException(status_code=401, detail="Unauthorized access")
    return api_key

@login_router.get("/api")
async def api_route(authorization: Annotated[str, Header()]):
    logger.debug(authorization)
    return authorization



