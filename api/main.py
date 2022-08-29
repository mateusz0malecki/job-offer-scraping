import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from settings import get_settings
from routes.job_offers import router as offers_router


def create_app() -> FastAPI:
    # Settings
    _settings = get_settings()

    # FastAPI
    app = FastAPI(
        docs_url="/docs",
        version="1.0.0"
    )

    # Routes
    app.include_router(offers_router)

    # Logging
    logging.basicConfig(
        filename='logs.log',
        filemode='a',
        level=logging.WARNING,
        format='%(asctime)s - %(levelname)s - %(module)s - %(message)s',
        encoding='utf-8'
    )

    # CORS
    origins = [
        "*"
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
