from fastapi import FastAPI
from api.v1.tenant import router as tenant_router
from api.v1.user import router as user_router
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
