import jwt
from datetime import datetime, timedelta
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from src.config import settings

default_cred = DefaultAzureCredential()
secret_client = SecretClient(vault_url=settings.KEYVAULT_URI, credential=default_cred)
_signing_key = secret_client.get_secret(settings.SECRET_NAME).value


def authenticate(username: str, password: str) -> bool:
    return username == 'admin' and password == 'secret'

def generate_token(subject: str) -> str:
    now = datetime.utcnow()
    payload = {
        'sub': subject,
        'iat': now,
        'exp': now + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, _signing_key, algorithm=settings.JWT_ALGORITHM)