from sqlalchemy.orm import Session

from models.parking import Parking, Parkseat
from schema.parking import ParkingBase, InParking


def register(db: Session, parking: ParkingBase): #, parkseat: InParking):
    parking = Parking(**parking.model_dump())
    db.add(parking)
    db.commit()
    db.refresh(parking)
    #
    # parkseat = Parkseat(**parkseat.model_dump())
    # db.add(parkseat)
    # db.commit()
    # db.refresh(parkseat)

    return parking # , parkseat


# 입차 시 paking에 저장되면 parkseat에도 저장 > 트리거
# CREATE OR REPLACE FUNCTION insert_into_parkseat()
# RETURNS TRIGGER AS $$
# BEGIN
# -- NEW는 삽입된 새로운 데이터를 의미
# -- Parkseat 테이블에 carnum과 barrier 값 삽입
# INSERT INTO parkseat (carnum, barrier)
# VALUES (NEW.carnum, FALSE);  -- carnum은 parking에서 가져오고, barrier는 기본값 FALSE
# RETURN NEW;  -- 트리거는 항상 NEW 값을 반환해야 함
# END;
# $$ LANGUAGE plpgsql;

# 출차 시 parkseat 데이터 삭제 > 트리거