from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from agent import ask_crm

app = FastAPI(title="AI-Powered CRM Assistant")

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


class ChatRequest(BaseModel):
    message: str


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@app.post("/chat")
def chat(request: ChatRequest):
    answer = ask_crm(request.message)

    return {
        "response": answer
    }