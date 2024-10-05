from enum import Enum
from typing import Optional, Union, Dict, Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar('T')


class Domain(str, Enum):
    TENANT_A = 'tenant_a'


class ResponseModel(BaseModel, Generic[T]):
    data: Optional[T] = None
    message: Optional[str] = None
    error: Optional[Union[Dict[Any, Any], str]] = None
