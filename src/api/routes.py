from fastapi import APIRouter, HTTPException, status, Body
from src.api.schemas import UserLoginRequest, TokenResponse, ErrorResponse, UserRegisterRequest, UserRegisterResponse
from src.auth.service import authenticate, generate_token, register_new_user, UserAlreadyExistsError
from src.utils import get_logger

temp_user_db = {}

logger = get_logger('auth-routes')
auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@auth_router.post(
    "/login",
    response_model=TokenResponse,
    summary="User Login",
    description="Authenticates a user and returns an access token upon success.",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": "Validation error: Username and password are required."
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "Authentication failed: Invalid username or password."
        },
    }
)
async def login(credentials: UserLoginRequest = Body(...)):
    if not credentials.username or not credentials.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username and password required" 
        )

    if not authenticate(credentials.username, credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = generate_token(credentials.username)
    logger.info('User %s logged in', credentials.username)
    return TokenResponse(access_token=token)
@auth_router.post(
    "/register",
    response_model=UserRegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Creates a new user account.",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": "Invalid input (e.g., password too short, invalid email)."
        },
        status.HTTP_409_CONFLICT: {
            "model": ErrorResponse,
            "description": "User with this username or email already exists."
        }
    }
)
async def register_user_route(user_data: UserRegisterRequest = Body(...)):
    try:
        logger.info(f"Attempting to register user: {user_data.username}")
        registered_user_details = register_new_user(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password
        )
        return UserRegisterResponse(
            username=registered_user_details["username"],
            email=registered_user_details["email"]
        )
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error during registration for {user_data.username}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during registration."
        )
