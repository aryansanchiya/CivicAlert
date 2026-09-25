from fastapi import FastAPI
from api.v1.tenant import router as tenant_router
from api.v1.user import router as user_router
from api.v1.auth import router as auth_router
from api.v1.crud_city import router as crud_city_router
from api.v1.road import router as road_router
from api.v1.incident import router as incident_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="CivicAlert API",
    version="1.0.0",
)


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tenant_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(crud_city_router)
app.include_router(road_router)
app.include_router(incident_router)

