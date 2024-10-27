from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text
from models.parking import Parking, Parkseat
from schema.parking import ParkingBase
from service.database import db_url

engine = create_engine(db_url, echo=True)


def create_triggers():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT name FROM sqlite_master WHERE type='trigger' AND name='after_insert_parking'"))
        if not result.fetchone():
            trigger_sql_parking = """
            CREATE TRIGGER after_insert_parking
            AFTER INSERT ON parking
            FOR EACH ROW
            BEGIN
                INSERT INTO parkseat (carnum, barrier) VALUES (NEW.carnum, NEW.barrier);
            END;
            """
            connection.execute(text(trigger_sql_parking))

        result = connection.execute(text("SELECT name FROM sqlite_master WHERE type='trigger' AND name='remove_parkseat'"))
        if not result.fetchone():
            trigger_sql_payment = """
            CREATE TRIGGER remove_parkseat
            AFTER INSERT ON payment
            FOR EACH ROW
            BEGIN
                DELETE FROM parkseat WHERE carnum = NEW.carnum;
            END;
            """
            connection.execute(text(trigger_sql_payment))


def register(db: Session, parking: ParkingBase):
    parking = Parking(**parking.model_dump())
    db.add(parking)
    db.commit()
    db.refresh(parking)

    return parking


def search(db: Session, parknum: str):
    query = (
        db.query(Parkseat.carnum, Parking.intime)
        .join(Parking, Parking.carnum == Parkseat.carnum)
        .filter(Parkseat.carnum.like(f"%{parknum}"))
    )
    result = query.all()
    return result


def set_outtime(db: Session, carnum: str):
    parking = db.query(Parking).filter(Parking.carnum == carnum).first()

    if not parking:
        return {"error": "Car not found"}

    parking.outtime = datetime.now()
    db.commit()

    total_time = parking.outtime - parking.intime
    total_minutes = total_time.total_seconds() / 60

    rate_10min = 1500       # 회차시간 15분 / 10분당 1500원
    total_fee = int((max(0, total_minutes - 15) / 10) * rate_10min)

    return {
        "carnum": parking.carnum,
        "intime": parking.intime,
        "outtime": parking.outtime,
        "total_minutes": total_minutes,
        "total_fee": total_fee
    }
