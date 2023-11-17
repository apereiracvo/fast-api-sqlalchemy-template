import asyncio
import subprocess
import sys

import spacy
import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import exceptions
from app.api.sample import router as sample_router
from app.config import settings
from app.db.deps import set_db
from app.db.exceptions import DatabaseValidationError


def get_app() -> FastAPI:
    _app = FastAPI(
        title=settings.SERVICE_NAME,
        debug=settings.DEBUG,
        dependencies=[Depends(set_db)],
    )
    _app.include_router(sample_router, prefix="/api")

    _app.add_exception_handler(
        DatabaseValidationError,
        exceptions.database_validation_exception_handler,
    )

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app


app = get_app()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, timeout_keep_alive=3600)
