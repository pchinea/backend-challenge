from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID

from app.adapters.db.tables.base import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    pass
