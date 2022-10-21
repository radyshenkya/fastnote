from urllib.request import Request
from fastapi import Body, FastAPI, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

from utils import generate_user_token
from SqliteClasses import SqlNotes, SqlNote

TEMPLATES_DIR_PATH = "./templates"
STATIC_DIR_PATH = "./static"
API_PREFIX = "/api/"

notes = SqlNotes()
app = FastAPI()

templates = Jinja2Templates(directory=TEMPLATES_DIR_PATH)
app.mount("/static", StaticFiles(directory=STATIC_DIR_PATH))

# REST API

# GET /api/get_token - generates token
@app.get(API_PREFIX + "get_token")
def get_token():
    return {"token": generate_user_token()}


# GET /api/{token}/note
@app.get(API_PREFIX + "{token}/note")
def get_notes(token: str):
    return {"ids": [el.get_id() for el in notes.get_user_notes(token)]}


# GET /api/{token}/note/{id}
@app.get(API_PREFIX + "{token}/note/{id}")
def get_note_details(token: str, id: str):
    note = None

    # Checking is note exists and this user can view it
    try:
        note = notes.get_by_id(id)
        assert note.can_view(token)
    except Exception as e:
        return JSONResponse(
            content={"error": "Can not find this note"},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return {
        "id": note.get_id(),
        "text": note.get_text(),
        "is_private": note.get_is_private(),
    }


# POST /api/{token}/note/ BODY: json object like {"text": "text", "is_private": false}
@app.post(API_PREFIX + "{token}/note", status_code=status.HTTP_201_CREATED)
def add_note(token: str, text=Body(), is_private=Body()):
    notes.new_note(token, text, bool(is_private))
    return {"ok": True}


# PATCH /api/{token}/note/{id} BODY: json object like {"text": "text", "is_private": false}
@app.patch(API_PREFIX + "{token}/note/{id}", status_code=status.HTTP_200_OK)
def update_note(
    token: str, id: str, text=Body(embed=True), is_private=Body(embed=True)
):
    note = None

    try:
        note = notes.get_by_id(id)
    except Exception as e:
        return JSONResponse(
            content={"error": "Can not find this note"},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    if not note.is_owner(token):
        return JSONResponse(
            content={"error": "Can not modify this note"},
            status_code=status.HTTP_403_FORBIDDEN,
        )

    note.set_is_private(is_private)
    note.set_text(text)

    return {"ok": True}


# DEFAULT PAGES
# GET /
@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# GET /{note_id}
@app.get("/{note_id}")
def note_details(request: Request, note_id: str):
    note = None
    error = None

    try:
        note = notes.get_by_id(note_id)
        assert note.can_view("")
    except:
        error = "Нет записи с таким ID"
        note = None

    return templates.TemplateResponse(
        "note_details.html", {"request": request, "error": error, "note": note}
    )
