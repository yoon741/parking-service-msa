from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schema.parking import ParkingBase
from service.database import get_db
from service.parking import register, carlists, set_outtime

router = APIRouter()

# 입차 시 시간 저장
@router.post('/carregist')
async def new_parking(parking: ParkingBase, db:Session=Depends(get_db)):
    print(parking)
    return register(db, parking)


# 출차 시 주차한 차 4자리번호로 조회한 목록 = parknum
@router.get('/carlists/{parknum}')
async def search_by_carnum(parknum: str, db: Session = Depends(get_db)):
    return carlists(db, parknum)

# 출차시 결제를 위한 내역(입차 중인 parking, payment 데이터)
@router.get('/outregist/{carnum}')
async def outpark(carnum: str, db: Session = Depends(get_db)):
    return set_outtime(db, carnum)