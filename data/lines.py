import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Lines(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'lines'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    stations = sqlalchemy.Column(sqlalchemy.String, nullable=True)
