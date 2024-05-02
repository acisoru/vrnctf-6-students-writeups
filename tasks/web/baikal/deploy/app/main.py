import random
import string

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

flag = "vrnctf{b357_w473r_1n_7h3_w0rld}"

acc_login = "Dobroslav"
acc_password = "SlavyaneNavsegda"

two_factor_tokens_tries = {
    "TestTokenXXXZZZ": 500
}

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def random_token():
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(20))


@app.get('/', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )


@app.get('/register', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        request=request, name="register.html"
    )


@app.get('/login', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        request=request, name="login.html",
        context={"message": None}
    )


@app.post('/login')
async def root(request: Request):
    form_data = await request.form()
    username = form_data.get("username")
    password = form_data.get("password")

    if not username or not password or username != acc_login or password != acc_password:
        return templates.TemplateResponse(
            request=request, name="login.html",
            context={"message": "Неверное имя или пароль"}
        )

    factor_token = random_token()

    two_factor_tokens_tries[factor_token] = 0

    return templates.TemplateResponse(
        request=request, name="2fa.html",
        context={"message": None,
                 "factor_token": factor_token}
    )


@app.post('/2fa')
async def root(request: Request):
    form_data = await request.form()
    factor_token = form_data.get("factor_token")

    two_factor_tokens_tries[factor_token] = two_factor_tokens_tries[factor_token] + 1

    if two_factor_tokens_tries[factor_token] > 500:
        return templates.TemplateResponse(
            request=request, name="flag.html",
            context={"flag": flag}
        )
    else:
        return templates.TemplateResponse(
            request=request, name="2fa.html",
            context={"message": "Неверный код.",
                     "factor_token": factor_token}
        )
