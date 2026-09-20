from enum import Enum
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict

class TenantType(str, Enum):
    """Enum representing the type of tenant."""

    INDIVIDUAL = "individual"
    GOVERNMENT_AGENCY = "government_agency"
    MUNICIPALITY = "municipality"

class TenantStatus(str, Enum):
    """Enum representing the status of a tenant."""

    PENDING = "pending"
    ACTIVE = "active"
    INACTIVE = "inactive"

class TenantCreate(BaseModel):
    """Schema for creating a new tenant."""

    name: str = Field(
        ...,
        max_length=255,
        min_length=2,
        description="The name of the tenant."
    )

    city_id: int = Field(
        ...,
        description="The ID of the city associated with the tenant."
    )

    code: str = Field(
        ...,
        max_length=100,
        min_length=2,
        description="A unique code for the tenant."
    )

    type: TenantType = Field(
        default=TenantType.MUNICIPALITY,
        description="The type of the tenant."
    )

    status: TenantStatus = Field(
        default=TenantStatus.PENDING,
        description="The status of the tenant."
    )

class TenantResponse(BaseModel):
    """Schema for tenant response."""

    id: UUID
    name: str
    city_id: int
    code: str
    type: TenantType
    status: TenantStatus

    model_config = ConfigDict(from_attributes=True)