import sqlalchemy
from .db_session import SqlAlchemyBase


class Classes(SqlAlchemyBase):
    __tablename__ = 'classes'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    spells_list = sqlalchemy.Column(sqlalchemy.String)
