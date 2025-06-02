import jwt
from datetime import datetime, timedelta, timezone
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from src.config import settings
from src.utils import get_logger

logger = get_logger(__name__)

_signing_key: str
if settings.KEYVAULT_URI and settings.SECRET_NAME and settings.KEYVAULT_URI.startswith('https://'):
    logger.info(f"Attempting to fetch JWT signing key from Azure Key Vault: {settings.KEYVAULT_URI}")
    try:
        default_cred = DefaultAzureCredential()
        secret_client = SecretClient(vault_url=settings.KEYVAULT_URI, credential=default_cred)
        _signing_key = secret_client.get_secret(settings.SECRET_NAME).value
        logger.info("Successfully fetched JWT signing key from Azure Key Vault.")
    except Exception as e:
        logger.error(f"Failed to fetch secret from Azure Key Vault: {e}. Falling back to local signing key if available.")
        if not settings.JWT_LOCAL_SIGNING_KEY:
            raise ValueError("Azure Key Vault access failed and no JWT_LOCAL_SIGNING_KEY is set.") from e
        _signing_key = settings.JWT_LOCAL_SIGNING_KEY
        logger.warning("Using local JWT signing key due to Azure Key Vault access failure.")
else:
    logger.warning("Azure Key Vault URI/Secret Name not configured or URI is invalid. Using local JWT signing key for MVP.")
    if not settings.JWT_LOCAL_SIGNING_KEY:
        raise ValueError("Azure Key Vault not configured and no JWT_LOCAL_SIGNING_KEY is set.")
    _signing_key = settings.JWT_LOCAL_SIGNING_KEY
    logger.info("Using local JWT signing key.")

# Uso em memória enquanto não temos acesso ao Azure gratuitamente...
# apenas um placeholder para o MVP, não vai persistir quando a aplicação reiniciar
temp_user_db = {}
# ------------------------------------------------------------

# --- para futuras integrações para persistir no banco real... ---
# from passlib.context import CryptContext
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#
# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)
#
# def get_password_hash(password):
#     return pwd_context.hash(password)
# ---------------------------------------------------------------------------

class UserAlreadyExistsError(Exception):
    pass

def register_new_user(username: str, email: str, password: str) -> dict:
    if username in temp_user_db:
        raise UserAlreadyExistsError("Username already registered.")
    for _, user_details in temp_user_db.items():
        if user_details['email'] == email:
            raise UserAlreadyExistsError("Email already registered.")

    # em um aplicativo real, faremos um hash do password:
    # hashed_password = get_password_hash(password)
    # Apenas para MVP, não irá para Produçao
    temp_user_db[username] = {
        "username": username,
        "email": email,
        "password": password  # Hash password em produçao...
    }
    logger.info(f"User {username} registered successfully.")
    return {"username": username, "email": email}


def authenticate(username: str, password: str) -> bool:
    if username == 'admin' and password == 'secret':
        return True

    user_in_db = temp_user_db.get(username)
    if user_in_db:
        if user_in_db['password'] == password:
            return True
    return False


def generate_token(subject: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        'sub': subject,
        'iat': now,
        'exp': now + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, _signing_key, algorithm=settings.JWT_ALGORITHM)