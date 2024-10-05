from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from controllers.user.base_user import BaseUser
from database import get_db
from schemas import Domain
from schemas.output.user import BaseUserAll
from utils import map_domain_to_class, map_response_model_output

tag = "user"
router = APIRouter(prefix=f"/{tag}", tags=[tag.capitalize()])

domain_mapping = map_domain_to_class(tag, BaseUser)


@router.get("",
            response_model=map_response_model_output(BaseUserAll, tag)
            )
def all_users(db: Session = Depends(get_db), domain: Domain = Header(None)):
    user_object = domain_mapping[domain]
    return user_object.get_all_users(db)
