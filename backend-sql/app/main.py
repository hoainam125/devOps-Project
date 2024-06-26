from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from .extra import config
from .routes import auth


config = config.get_config()

docs = '/api/docs' if not config.PRODUCTION else None
redoc= '/api/redoc' if not config.PRODUCTION else None
openapi = '/api/openapi.json' if not config.PRODUCTION else None
app = FastAPI(docs_url = docs, redoc_url = redoc, openapi_url = openapi,debug=True)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host=config.HOST, port=8001)
