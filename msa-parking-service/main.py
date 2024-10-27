import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import parking
from service.database import create_tables
from service.parking import create_triggers

app = FastAPI()

app.include_router(parking.router)

# CORS 설정
origins = [
    "http://localhost:3000", # 허용할 프론트엔드 도메인
    "http://127.0.0.1:3000"  # 허용할 프론트엔드 IP
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=['*'],
    allow_headers=['*']
)

if __name__ == '__main__':
    create_tables()
    create_triggers()
    uvicorn.run('main:app', port=8000, reload=True)

