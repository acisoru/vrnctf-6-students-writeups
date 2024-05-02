import uvicorn
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.staticfiles import StaticFiles

client: FastAPI = FastAPI(title="Museum Project")

client.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
templates = Jinja2Templates(directory="templates")
client.mount("/static", StaticFiles(directory="static"), name="static")


@client.get("/")
def main_page(request: Request):
    return templates.TemplateResponse(name="main.html", request=request)


@client.get('/feedback')
def feedback_page(request: Request):
    return templates.TemplateResponse(name="feedback.html", request=request)
