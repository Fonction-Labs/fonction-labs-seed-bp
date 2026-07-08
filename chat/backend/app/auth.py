"""Bearer token authentication dependency for FastAPI."""

from __future__ import annotations

import os

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

_bearer = HTTPBearer()


def require_auth(credentials: HTTPAuthorizationCredentials = Depends(_bearer)) -> str:
    expected = os.getenv("ACCESS_TOKEN")
    if not expected:
        raise HTTPException(status_code=500, detail="ACCESS_TOKEN not configured")
    if credentials.credentials != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials
