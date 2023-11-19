from typing import List
from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks, Request, Query
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import httpx
from .test import esupload
from .querybuidler import esqbuild
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
templates = Jinja2Templates(directory="server/templates")

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
esurl = ""

async def upload_to_external_server(file_content: str, name: str):
    async with httpx.AsyncClient() as client:
        response = await esupload(file=file_content)
        if response.status_code != 200 and response.status_code != 201:
            print(f"Failed to upload JSON file. Status code: {response.status_code} and file name: {name}")

@app.post("/upload/")
async def upload_json(files: list[UploadFile] = File(...), background_tasks: BackgroundTasks = None):
    try:
        # Read the content of the uploaded file
        #uploaded_files = []
        for file in files:
            print(file.filename)
            contents = await file.read()
            # Schedule the asynchronous upload to the external server
            background_tasks.add_task(upload_to_external_server, contents, file.filename)
            # uploaded_files.append({"filename": file.filename, "contents": contents.decode("utf-8")})

        return {"message": "JSON files upload scheduled successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/ui")
async def qui(request: Request):
    return templates.TemplateResponse("test.html", {"request": request})

@app.post("/query")
async def get_query(request: Request):
    #print('in post')
    res = await request.json()
    #print(res)
    queryres = esqbuild(res)
    hits = queryres['hits']['hits']
    for i in range(len(hits)):
        hits[i] = hits[i]['_source']
    #print(hits)
    return templates.TemplateResponse("result.html", {"request": request, "log_entries": hits})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server.api:app", host="0.0.0.0", port=8000, reload=True)
