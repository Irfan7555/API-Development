from database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    # published = Column(Boolean, default=True)  This is not the correct method to set default
    published = Column(Boolean, server_default='TRUE', nullable=False)


    

