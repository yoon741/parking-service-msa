from datetime import datetime

from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Parking(Base):
    __tablename__ = 'parking'

    pno = Column(Integer, primary_key=True, autoincrement=True, index=True)
    carnum = Column(String(10), nullable=False)
    barrier = Column(String(5), nullable=False, default='0')
    intime = Column(DateTime, default=datetime.now)
    outtime = Column(DateTime, default=datetime.now)


class Parkseat(Base):
    __tablename__ = 'parkseat'

    carnum = Column(String(10), primary_key=True, nullable=False)
    barrier = Column(String(5), nullable=False, default='0')