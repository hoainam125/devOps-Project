from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from extra import config
from routes import auth, panel


config = config.get_config()
is_production = bool(config.PRODUCTION)
if not is_production:
    docs = '/api/docs'
    redoc= '/api/redoc'
    openapi = '/api/openapi.json'
else:

    docs = None
    redoc = None
    openapi = None
app = FastAPI(docs_url = docs, redoc_url = redoc, openapi_url = openapi)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(panel.router, prefix="/api/panel")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host=config.HOST, port=config.PORT)
