from pydantic import BaseModel, ConfigDict, Field


class CompanyRequest(BaseModel):
    """Request body for /analyze - accepts 'domain' from frontend."""
    model_config = ConfigDict(populate_by_name=True)
    company_domain: str = Field(..., alias="domain")