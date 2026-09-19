from fastapi import FastAPI
from api.v1.tenant import router as tenant_router
from api.v1.user import router as user_router
from api.v1.auth import router as auth_router
from api.v1.crud_city import router as crud_city_router

app = FastAPI(
    title="CivicAlert API",
    version="1.0.0",
)


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

app.include_router(tenant_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(crud_city_router)