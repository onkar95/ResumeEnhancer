from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import RedirectResponse

from app.core.config import settings
from app.core.security import create_access_token
from app.dependencies import get_current_user
from app.services.usage_service import remaining_quota
from app.services.user_service import upsert_google_user

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])

oauth = OAuth()
oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


@router.get("/login")
async def login(request: Request):
    return await oauth.google.authorize_redirect(
        request, settings.GOOGLE_REDIRECT_URI
    )


@router.get("/callback")
async def callback(request: Request):
    token = await oauth.google.authorize_access_token(request)

    userinfo = token.get("userinfo")
    if not userinfo:
        userinfo = await oauth.google.userinfo(token=token)

    user = upsert_google_user(
        google_id=userinfo["sub"],
        email=userinfo["email"],
        name=userinfo.get("name"),
        picture=userinfo.get("picture"),
    )

    jwt_token = create_access_token({"sub": user["user_id"]})

    response = RedirectResponse(url=settings.FRONTEND_URL)
    response.set_cookie(
        key="access_token",
        value=jwt_token,
        httponly=True,
        samesite="lax",
        secure=settings.COOKIE_SECURE,
        max_age=60 * 60 * 24 * 7,
        path="/",
    )
    return response


@router.get("/me")
def me(current_user: dict = Depends(get_current_user)):
    return {
        "user_id": current_user["user_id"],
        "email": current_user["email"],
        "name": current_user.get("name"),
        "picture": current_user.get("picture"),
        "remaining_quota": remaining_quota(current_user["user_id"]),
    }


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token", path="/")
    return {"success": True}