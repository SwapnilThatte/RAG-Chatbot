import os
import uuid
from fastapi import FastAPI, Request, File, UploadFile, Form
from run_model import generate_response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from rag_util import Create_RAG_Prompt, ProcessDocuments
import time
import bleach

class DataModel(BaseModel):
    data: str
    id : str = ""
    chatID :str = Field(..., min_length=36, description="Chat ID must not be empty")


app = FastAPI(
    docs_url=None,       # disables /docs
    redoc_url=None,      # disables /redoc
    openapi_url=None     # disables /openapi.json
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

chat_history = {}
CHAT_START_TIME = time.time()



@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    chatID = uuid.uuid4()
    return templates.TemplateResponse("index.html", {"request" : request, "chatID" : chatID})


@app.post("/generate")
async def generate(data: DataModel):
    dataID = bleach.clean(data.id)
    if dataID == "":
        input_text = bleach.clean(data.data)
        history = chat_history[data.chatID] = [] if data.chatID not in chat_history else chat_history[data.chatID]

        llm_response = generate_response(prompt=input_text, history=history)
        
        if data.chatID not in chat_history:
            chat_history[data.chatID] = []
        chat_history[data.chatID].append({"role": "user", "content": input_text})
        chat_history[data.chatID].append({"role": "assistant", "content": llm_response})

        return {"llm_response" : llm_response}
    else :
        input_text = bleach.clean(data.data)
        prompt, context = Create_RAG_Prompt(input_text, chatID=data.chatID, history=chat_history[data.chatID] if chat_history[data.chatID] else [])

        llm_response = generate_response(prompt=prompt, context=context)
       
        if data.chatID not in chat_history:
            chat_history[data.chatID] = []
        chat_history[data.chatID].append({"role": "user", "content": input_text})
        chat_history[data.chatID].append({"role": "assistant", "content": llm_response})

        return {"llm_response" : llm_response}


def isValidPDF(file):
    if not file.filename.endswith(".pdf") or file.content_type != "application/pdf":
        return False
    return True


@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...), chatID:str = Form(...)):
    fileID = uuid.uuid4()
    save_path = f"./uploads/{fileID}.pdf"

    # Ensure uploads directory exists
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    if isValidPDF(file):
        with open(save_path, "wb") as f:
            f.write(await file.read())
    # print(save_path)

        ProcessDocuments(save_path, chatID)
        return {"filename": fileID, "message": "PDF uploaded successfully."}
    else :
        return {"filename" : "UPLOADED_FILE", "message" : "Uploaded File is not a valid PDF."}



