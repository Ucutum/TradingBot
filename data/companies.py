import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class Company(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = "companies"

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    code = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    stocks = orm.relationship("Stock", back_populates='company', uselist=True)
    model = sqlalchemy.Column(sqlalchemy.String)
