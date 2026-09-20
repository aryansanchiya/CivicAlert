from sqlalchemy import select, func
from sqlalchemy.orm import Session

from models.tenant import Tenant
from models.city import City
from schemas.tenant import TenantCreate


def register_tenant(
    db: Session,
    tenant_data: TenantCreate,
) -> Tenant:

    # 1. Normalize tenant code
    tenant_code = tenant_data.code.strip().upper()

    # 2. Normalize tenant name
    tenant_name = " ".join(tenant_data.name.strip().split())

    # 3. Check if tenant with same name already exists
    existing_tenant = db.scalar(
        select(Tenant).where(
            func.lower(Tenant.name) == tenant_name.lower()
        )
    )

    if existing_tenant:
        raise ValueError(
            f"A tenant with the name '{tenant_name}' already exists."
        )

    # 4. Verify that the city exists
    city = db.scalar(
        select(City).where(
            City.id == tenant_data.city_id
        )
    )

    if not city:
        raise ValueError(
            f"City with ID '{tenant_data.city_id}' does not exist."
        )

    # 5. Create tenant
    tenant = Tenant(
        name=tenant_name,
        city_id=tenant_data.city_id,
        code=tenant_code,
        type=tenant_data.type.value,
        status=tenant_data.status.value,
    )

    db.add(tenant)
    db.commit()
    db.refresh(tenant)

    return tenant