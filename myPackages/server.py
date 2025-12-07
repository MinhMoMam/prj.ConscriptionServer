from fastapi import FastAPI, Request, Form, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import myPackages.dataContainer as dc
from typing import Dict, Any

excelFile = "data/CƠ CẤU HỆ THỐNG.xlsx"
settingFile = "setting/labelConfig.yaml"
dataCon = dc.dataContainer(excelFile,settingFile)

items = ["a","b","c","d"]
# Mount static folder for CSS/JS/images
templates = Jinja2Templates(directory="templates")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    content = dataCon.getRootParam();
    content["request"] = request
    return templates.TemplateResponse("root.html", content)

@app.get("/ObjectSearching", response_class=HTMLResponse)
def ObjectSearching(request: Request,Name: str="",YearOfBirth: str="",Commune: str=""):
    content = dataCon.returnSearchResult(Name,YearOfBirth,Commune);
    content["request"] = request
    return templates.TemplateResponse("root.html", content)

@app.get("/details", response_class=HTMLResponse)
def detailsView(request: Request,Name: str="",YearOfBirth: str="",Commune: str=""):
    content = dataCon.retObjDetailInformation(Name,YearOfBirth,Commune);
    content["request"] = request
    return templates.TemplateResponse("detailInfor.html", content)

@app.post("/submit-military-data/")
async def create_items(request: Request):
    form = await request.form()  # This captures ALL form fields
    data = dict(form)            # Convert to dictionary
    dataCon.updateDataFrame(data)
    return Response(status_code=204)  # No Content
