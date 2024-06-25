from fastapi import FastAPI
from app.api import auth
from app.core import config, database
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

config = settings()
app = FastAPI(docs_url='/api/docs' if not config['PROD'] else None,
              redoc_url='/api/redoc' if not config['PROD'] else None,
              openapi_url='/api/openapi.json' if not config['PROD'] else None)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    database.Base.metadata.create_all(bind=database.engine)
    print("Connect Database")
    uvicorn.run(app, host=config.HOST, port=config.PORT)

