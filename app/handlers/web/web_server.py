from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import pathlib

app = FastAPI()

BASE_DIR = pathlib.Path(__file__).parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

class LoginRequest(BaseModel):
    email: str
    password: str
    initData: str = None

@app.get("/", response_class=HTMLResponse)
async def serve_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/api/login")
async def handle_login(data: LoginRequest):
    # Here you connect to your app/api/sign_in.py logic
    # example: status = await sign_in_user(data.email, data.password)
    
    if data.email and data.password:
        return {"success": True, "message": "Authenticated successfully"}
    return {"success": False, "message": "Invalid credentials"} 

@app.get("/terms", response_class=HTMLResponse)
async def serve_terms_page(request: Request):
    return templates.TemplateResponse("terms.html", {"request": request})

@app.post("/api/accept-terms")
async def handle_accept_terms(data: dict):
    # Здесь сохраняете статус согласия пользователя в БД
    return {"success": True, "message": "Соглашение успешно принято"}

@app.get("/profile", response_class=HTMLResponse)
async def serve_profile(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})

# Add these page routes
@app.get("/feedback", response_class=HTMLResponse)
async def serve_feedback(request: Request):
    return templates.TemplateResponse("feedback.html", {"request": request})

# API for feedback submission
class FeedbackModel(BaseModel):
    type: str
    text: str
    is_anonymous: bool
    initData: str = None

@app.post("/api/feedback")
async def handle_feedback(data: FeedbackModel):
    # Save feedback to DB or forward to Telegram admin
    return {"success": True}