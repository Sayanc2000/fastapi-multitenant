from sqlalchemy.orm import Session

from schemas import ResponseModel
from schemas.output.user import BaseUserDisplay
from utils import dynamic_import_module


class BaseUser:
    def __init__(self, domain: str = None):
        self.domain = domain
        self.models = dynamic_import_module(domain)

    def get_all_users(self, db: Session):
        users = db.query(self.models.User).all()
        users_data = [BaseUserDisplay.from_orm(user) for user in users]
        return ResponseModel(data={"users": users_data}, message="Users fetched successfully", error=None)
