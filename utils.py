import importlib
import os
from typing import Union

from fastapi import HTTPException, status, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from schemas import Domain, ResponseModel

ACCESS_TOKEN_EXPIRE_MINUTES = 30


class DomainCheckMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.skip_paths = ["/docs", "/redoc", "/openapi.json", "/favicon.ico", "/", "/auth/domain-tag", "/auth/login"]

    async def dispatch(self, request: Request, call_next):
        if request.url.path in self.skip_paths:
            return await call_next(request)
        domain = request.headers.get('domain')
        if not domain:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid domain",
            )
        if domain not in Domain.__members__.values():
            return JSONResponse(
                status_code=403,
                content={"message": "Invalid 'domain' value"}
            )
        response = await call_next(request)
        return response


domain_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid domain",
)

authorise_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

permission_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Beyond permission scope"
)


def dynamic_import_module(package_name: str, module_name: str = 'models'):
    try:
        full_module_name = f"{package_name}.{module_name}"
        module = importlib.import_module(full_module_name)
        return module
    except ImportError as e:
        raise ImportError(f"Could not import {module_name} from {package_name}: {e}")


def map_domain_to_class(tag: str, base_class):
    files = os.listdir(f"controllers/{tag}")
    classes_in_user_folder = [file.split("_")[0] for file in files if file.endswith(".py")]
    classes_in_user_folder.remove('base')
    enum_class_list = [domain.value for domain in Domain]

    domain_mapping = {}

    for domain in enum_class_list:
        if domain in classes_in_user_folder:
            # instantiate the class
            module = dynamic_import_module("controllers", f"{tag}.{domain}_{tag}")
            class_type_name = tag.replace("_", " ").title().replace(" ",
                                                                    "")  # convert to call name type Ex: call_analysis -> CallAnalysis
            class_name = f"{domain.capitalize()}{class_type_name}"
            # TODO - instead of hard coding the class based name, we can dynamically get the class name from reading the file
            user_flow = getattr(module, class_name)(domain)
            domain_mapping[domain] = user_flow
        else:
            # instantiate the base class
            user_flow = base_class(domain)
            domain_mapping[domain] = user_flow

    return domain_mapping


def map_response_model(BaseSchema, tag: str):
    domain_list = [domain.value for domain in Domain]
    base_schema_name: str = BaseSchema.__name__
    schema_list = []
    for domain in domain_list:
        domain_schema_name = base_schema_name.replace('Base', domain.capitalize())
        try:
            module = dynamic_import_module(domain, f"schemas.{tag}")
        except ImportError:
            continue
        if hasattr(module, domain_schema_name):
            schema_class = getattr(module, domain_schema_name)
            schema_list.append(schema_class)
    # if len(schema_list) < len(domain_list):
    schema_list.append(BaseSchema)

    return Union[tuple(schema_list)]


def map_response_model_input(BaseSchema, tag: str):
    domain_list = [domain.value for domain in Domain]
    base_schema_name: str = BaseSchema.__name__
    schema_list = []
    for domain in domain_list:
        domain_schema_name = base_schema_name.replace('Base', domain.capitalize())
        try:
            module = dynamic_import_module(domain, f"schemas.input.{tag}")
        except ImportError:
            continue
        if hasattr(module, domain_schema_name):
            schema_class = getattr(module, domain_schema_name)
            schema_list.append(schema_class)
    # if len(schema_list) < len(domain_list):
    schema_list.append(BaseSchema)

    return Union[tuple(schema_list)]


def map_response_model_output(BaseSchema, tag: str):
    domain_list = [domain.value for domain in Domain]
    base_schema_name: str = BaseSchema.__name__
    schema_list = []
    for domain in domain_list:
        domain_schema_name = base_schema_name.replace('Base', domain.capitalize())
        try:
            module = dynamic_import_module(domain, f"schemas.output.{tag}")
        except ImportError as e:
            print(e)
            continue
        if hasattr(module, domain_schema_name):
            schema_class = getattr(module, domain_schema_name)
            schema_list.append(schema_class)
    # if len(schema_list) < len(domain_list):
    schema_list.append(ResponseModel[BaseSchema])

    return Union[tuple(schema_list)]
