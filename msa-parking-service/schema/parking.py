from datetime import datetime

from pydantic import BaseModel


class ParkingBase(BaseModel):
    carnum: str

class InParking(ParkingBase):
    pno: int
    intime: datetime
    barrier: str

    class Config:
        from_attribute=True

# class outParking(ParkingBase):
#     outtime: datetime
#
#     class Config:
#         from_attribute=True