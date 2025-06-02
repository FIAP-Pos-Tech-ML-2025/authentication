from fastapi import FastAPI
from src.config import settings
from src.api.routes import auth_router
from src.utils import get_logger
import uvicorn

logger = get_logger(__name__)

app = FastAPI(title=settings.APP_NAME)

app.include_router(auth_router)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=5000, log_level=settings.LOG_LEVEL.lower())