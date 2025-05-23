from database import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    # published = Column(Boolean, default=True)  This is not the correct method to set default
    published = Column(Boolean, server_default='TRUE', nullable=False)
    # created_at = Column(TIMESTAMP(timezone=True), server_default='now()')
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))


