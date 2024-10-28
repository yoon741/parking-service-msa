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
            # 차량번호 입력 해 parking 테이블에 저장하면 trigger 작동 (parkseat에 값 저장)
            trigger_sql_parking = """
            CREATE TRIGGER insert_parking
            AFTER INSERT ON parking
            FOR EACH ROW
            BEGIN
                INSERT INTO parkseat (carnum, barrier) VALUES (NEW.carnum, NEW.barrier);
            END;
            """
            connection.execute(text(trigger_sql_parking))

        result = connection.execute(text("SELECT name FROM sqlite_master WHERE type='trigger' AND name='remove_parkseat'"))
        if not result.fetchone():
            # 결제완료 시 payment 테이블에 저장 된 paydate에 값이 채워지면
            # parkseat에 동일한 carnum 데이터 삭제
            trigger_sql_payment = """
            CREATE TRIGGER remove_parkseat
            AFTER UPDATE ON payment
            FOR EACH ROW
            BEGIN
                IF OLD.paydate IS NULL AND NEW.paydate IS NOT NULL THEN
                    DELETE FROM parkseat WHERE carnum = NEW.carnum;
                END IF;
            END;
            """
            connection.execute(text(trigger_sql_payment))

# 입차
# 차량번호 입력 시 parking테이블에 저장
def register(db: Session, parking: ParkingBase):
    parking = Parking(**parking.model_dump())
    db.add(parking)
    db.commit()
    db.refresh(parking)

    return parking

# 입차 내역 전부 조회
def carlists(db: Session, parknum: str):
    query = (
        db.query(Parkseat.carnum, Parking.intime)
        .join(Parking, Parking.carnum == Parkseat.carnum)
        .filter(Parkseat.carnum.like(f"%{parknum}"))
    )
    result = query.all()
    return result

# 출차
# carlists에서 주차한 차를 선택해서 outregist페이지로 넘어갈 때 outtime 저장
def set_outtime(db: Session, carnum: str):
    parking = db.query(Parking).filter(Parking.carnum == carnum).first()

    if not parking:
        return {"error": "Car not found"}

    parking.outtime = datetime.now()
    db.commit()

# 차량 정보 출력
    # total_time = parking.outtime - parking.intime
    # total_minutes = total_time.total_seconds() / 60
    #
    # rate_10min = 1500       # 회차시간 15분 / 10분당 1500원
    # total_fee = int((max(0, total_minutes - 15) / 10) * rate_10min)
    #
    # return {
    #     "carnum": parking.carnum,
    #     "intime": parking.intime,
    #     "outtime": parking.outtime,
    #     "total_minutes": total_minutes,
    #     "total_fee": total_fee
    # }
