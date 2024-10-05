from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import engine
from tenant_a.models import Base as tenantABase


@asynccontextmanager
async def lifespan(app: FastAPI):
    tenantABase.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan, title="FastAPI Multi Tenant")


@app.get("/")
def read_root():
    return {"Hello": "World"}
