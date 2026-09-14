from sqlalchemy import select, func
from sqlalchemy.orm import Session
from models.tenant import Tenant
from schemas.tenant import TenantCreate

def register_tenant(
        db:Session,
        tenant_data: TenantCreate,
) -> Tenant:



    #1. Normalize the tenant code to uppercase
    tenant_code = tenant_data.code.strip().upper()

    #2. Check if a tenant with the same name already exists

    tenant_name = " ".join(tenant_data.name.strip().split())
    existing_tenant = db.scalar(
        select(Tenant).where(
            func.lower(Tenant.name) == tenant_name.lower()
        )
    )

    if existing_tenant:
        raise ValueError(f"A tenant with the name '{tenant_name}' already exists.")

    tenant = Tenant(
        name=tenant_name,
        code=tenant_data.code.strip().upper(),
        type=tenant_data.type.value,
        status=tenant_data.status.value,
    )

    db.add(tenant)
    db.commit()
    db.refresh(tenant)

    return tenant

