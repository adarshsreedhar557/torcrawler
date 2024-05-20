from sqlalchemy import create_engine, Column, String, Text, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

Base = declarative_base()

class CrawledData(Base):
    __tablename__ = 'crawled_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, unique=True)
    content = Column(Text)

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
