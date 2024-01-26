import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class Stock(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = "stocks"

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True, autoincrement=True)
    data_type = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    created_datetime = sqlalchemy.Column(
        sqlalchemy.DateTime,
        default=datetime.datetime.now)
    datetime = sqlalchemy.Column(sqlalchemy.DateTime)
    open = sqlalchemy.Column(sqlalchemy.Integer)
    close = sqlalchemy.Column(sqlalchemy.Integer)
    high = sqlalchemy.Column(sqlalchemy.Integer)
    low = sqlalchemy.Column(sqlalchemy.Integer)
    value = sqlalchemy.Column(sqlalchemy.Integer)
    is_predict = sqlalchemy.Column(sqlalchemy.Boolean)

    company_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('companies.id'))
    company = orm.relationship("Company", back_populates='stocks')