from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer
from jose import JWTError

from .jwt_handler import decode_token


class JWTBearer(HTTPBearer):
    def __init__(self, allowed_roles=None):
        super().__init__()
        self.allowed_roles = allowed_roles

    async def __call__(self, request: Request):
        credentials = await super().__call__(request)
        if credentials:
            try:
                payload = decode_token(credentials.credentials)
                if payload is None:
                    raise HTTPException(status_code=403, detail="Invalid token")
                role = payload.get("role")
                if self.allowed_roles and role not in self.allowed_roles:
                    raise HTTPException(
                        status_code=403, detail="Not enough permissions"
                    )
                return payload
            except JWTError:
                raise HTTPException(
                    status_code=403, detail="Invalid authentication credentials"
                )
        else:
            raise HTTPException(
                status_code=403, detail="Invalid authentication credentials"
            )
