
from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Parking(Base):
    __tablename__ = 'parking'

    pno = Column(Integer, primary_key=True, autoincrement=True, index=True)
    carnum = Column(String(10), nullable=False)
    barrier = Column(String(5), nullable=False, default='0')
    intime = Column(DateTime, default=datetime.now)
    outtime = Column(DateTime, nullable=True)


class Parkseat(Base):
    __tablename__ = 'parkseat'

    carnum = Column(String(10), primary_key=True, nullable=False)
    barrier = Column(String(5), nullable=False, default='0')

# 수정 필요
class Payment(Base):
    __tablename__ = 'payment'

    payid = Column(String(30), primary_key=True, index=True)
    payment = Column(String(50))
    paydate = Column(DateTime, nullable=True)
    parkingtime = Column(String(20), nullable=True)
    carnum = Column(String(10), ForeignKey('parking.carnum'))