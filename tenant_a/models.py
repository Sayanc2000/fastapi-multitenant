from base_models import UserMixin, NoteMixin
from database import get_base

Base = get_base('tenant_a')


class User(Base, UserMixin):
    __tablename__ = 'users'


class Note(Base, NoteMixin):
    __tablename__ = 'notes'
