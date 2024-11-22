from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from starlette.middleware.authentication import AuthenticationMiddleware

from core.security import JWTAuth
from users.routes import router as guest_router, user_router
from auth.route import router as auth_router

app = FastAPI()
app.include_router(user_router)
app.include_router(guest_router)
app.include_router(auth_router)

#add Middleware
app.add_middleware(AuthenticationMiddleware, backend=JWTAuth())

@app.get('/')
def health_check():
    return JSONResponse(content={"status": "Running"})
