from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.dependencies import get_db
from schemas.tenant import TenantCreate, TenantResponse
from services.tenant_service import register_tenant

router = APIRouter(
    prefix="/api/v1/tenants",
    tags=["tenants"],
)

@router.post("/register", response_model=TenantResponse, status_code=status.HTTP_201_CREATED)
def register_government_tenant(
    tenant_data : TenantCreate,
    db : Session = Depends(get_db)
):
    try:
        tenant = register_tenant(db, tenant_data)
        return tenant
    except ValueError as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))