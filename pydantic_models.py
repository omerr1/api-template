from pydantic import BaseModel, Field
from datetime import date

class PropertySchema(BaseModel):
    property_name: str = Field(max_length=100)
    address: str = Field(max_length=200)

class UnitSchema(BaseModel):
    property_id: int
    unit_number: str = Field(max_length=50)
    size: int = Field(gt=0)
    type: str = Field(max_length=50)

class LeaseSchema(BaseModel):
    unit_id: int
    tenant_id: int
    start_date: date
    end_date: date

class TenantSchema(BaseModel):
    tenant_id: int
