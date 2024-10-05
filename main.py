from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import engine
from routers.user import router as user_router
from tenant_a.models import Base as tenantABase


@asynccontextmanager
async def lifespan(app: FastAPI):
    tenantABase.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan, title="FastAPI Multi Tenant")
app.include_router(user_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
