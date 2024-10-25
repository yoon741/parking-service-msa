from fastapi import APIRouter, Depends
from sqlalchemy.orm import session

from schema.parking import ParkingBase
from service.database import get_db
from service.parking import register

router = APIRouter()

# 입차 시 시간 저장
@router.post('/parking')
async def new_parking(parking,parkseat: ParkingBase, db:session=Depends(get_db)):
    print(parking)
    return register(db, parking, parkseat)