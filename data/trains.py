import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Trains(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'trains'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    station1 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    station2 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    travel_time = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    line_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("lines.id"))

