from sqlalchemy import String,Integer,DateTime,Column
from database import Base

# creating our db model
class Blob(Base):
    __tablename__ = "blob"
    id = Column(Integer,primary_key=True,index = True)
    blob_url = Column(String)
    camera_id = Column(Integer)
    date = Column(DateTime)