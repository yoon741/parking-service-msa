from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schema.parking import ParkingBase
from service.database import get_db
from service.parking import register, search, set_outtime

router = APIRouter()


# 입차 시 시간 저장
@router.post('/parking')
async def new_parking(parking: ParkingBase, db:Session=Depends(get_db)):
    print(parking)
    return register(db, parking)


# 출차 시 주차한 차 4자리번호로 조회
@router.get('/search/{parknum}')
async def search_by_carnum(parknum: str, db: Session = Depends(get_db)):
    return search(db, parknum)


@router.get('/outpark/{carnum}')
async def outpark(carnum: str, db: Session = Depends(get_db)):
    return set_outtime(db, carnum)