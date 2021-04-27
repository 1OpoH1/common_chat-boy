import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Players(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'players'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    y_class = sqlalchemy.Column(sqlalchemy.Integer)
    level = sqlalchemy.Column(sqlalchemy.Integer)
    race = sqlalchemy.Column(sqlalchemy.String)
    speciality = sqlalchemy.Column(sqlalchemy.String)
    known_spells = sqlalchemy.Column(sqlalchemy.String)