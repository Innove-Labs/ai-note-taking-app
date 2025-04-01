from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, HTTPException, Response, Request, Depends

from configs.config import settings
from models import User
from schemas import UserSignup
from schemas.User import UserLogin
from utils import hash_password, verify_password
from utils.password import create_access_token, get_current_user

router = APIRouter()

oauth = OAuth()
oauth.register(
    "google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    authorize_params=None,
    access_token_url="https://oauth2.googleapis.com/token",
    access_token_params=None,
    client_kwargs={"scope": "openid email profile"},
)

@router.post("/signup")
async def signup(user_data: UserSignup):
    existing_user = await User.find_one(User.email == user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hash_password(user_data.password)
    )
    await user.create()
    return {"message": "User created successfully"}

@router.post("/login")
async def login(user_data: UserLogin, response: Response):
    user = await User.find_one(User.email == user_data.email)
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": user.email})
    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True, samesite="strict")
    return {"message": "Login successful"}


@router.get("/login/google")
async def login_google(request: Request):
    return await oauth.google.authorize_redirect(request, "http://localhost:8000/auth/google")


@router.get("/auth/google")
async def auth_google(request: Request, response: Response):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get("userinfo")

    user = await User.find_one(User.email == user_info["email"])
    if not user:
        user = User(
            email=user_info["email"],
            full_name=user_info["name"],
            google_id=user_info["sub"],
            picture=user_info.get("picture")
        )
        await user.create()

    access_token = create_access_token({"sub": user.email})
    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True, samesite="strict")
    return {"message": "Google login successful"}


@router.post("/logout")
async def logout(response: Response, _= Depends(get_current_user)):
    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}