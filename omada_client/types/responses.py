from typing import Generic, TypeVar
from pydantic import BaseModel, ConfigDict, Field

M = TypeVar("M", bound=BaseModel)
T = TypeVar("T")

class AuthorizationResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    access_token: str = Field(alias="accessToken")
    expires_in: int = Field(alias="expiresIn")
    refresh_token: str = Field(alias="refreshToken")

class ComplexResponseGeneric(BaseModel, Generic[T]):
    error_code: int | None = Field(alias="errorCode", default=None)
    msg: str | None = Field(None)
    result: T | None = Field(None)

class PaginationResponseGeneric(BaseModel, Generic[T]):
    total_rows: int = Field(alias="totalRows")
    current_page: int = Field(alias="currentPage")
    current_size: int = Field(alias="currentSize")
    data: list[T] | None = Field(None)

class IdResponseModel(BaseModel):
    id: str