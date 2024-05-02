import uvicorn
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from api.routers import feedback
from database import create_tables, anti_injection_func


def create_app() -> FastAPI:
    api = FastAPI(title="Museum Project")
    api.include_router(feedback.feedback_router, prefix="/api/feedback")

    return api


app: FastAPI = create_app()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)
templates = Jinja2Templates(directory="client/templates")
create_tables()
anti_injection_func()


if __name__ == '__main__':
    uvicorn.run(app)
