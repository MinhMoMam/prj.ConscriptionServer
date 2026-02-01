from fastapi import FastAPI, Request, Form, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import myPackages.dataContainer as dc
from typing import Dict, Any
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates


excelFile = "data/CƠ CẤU HỆ THỐNG.xlsx"
settingFile = "setting/labelConfig.yaml"
dataKey = ["Thuongtruap","Namsinh","Hovaten"]
searchingKey = ["Thuongtruap","Namsinh","Hovaten"]
dataCon = dc.dataContainer(excelFile,settingFile,dataKey,searchingKey)

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
def ObjectSearching(request: Request):
    params: dict = dict(request.query_params)
    content = dataCon.returnSearchResult(params)
    content["request"] = request
    return templates.TemplateResponse("root.html", content) 

@app.get("/details", response_class=HTMLResponse)
def detailsView(request: Request):
    params: dict = dict(request.query_params)
    content = dataCon.retObjDetailInformation(params)
    content["request"] = request
    return templates.TemplateResponse("detailInfor.html", content)

@app.post("/submit-military-data/")
async def create_items(request: Request):
    form = await request.form()  # This captures ALL form fields
    data = dict(form)            # Convert to dictionary
    dataCon.updateDataFrame(data)
    return Response(status_code=204)  # No Content


def gatherInformation(key,question,valueLabel,placeHodler):
    str = f'\n<div class="info-item">{question}: \n<input type="text" name="{key}" value="{valueLabel}" class="placeholder-input line-full" placeholder="{placeHodler}" required>\n</div>'
    return  str

templates.env.globals["gatherInformation"] = gatherInformation

def gatherGroupInformation(key,valueLabel,placeHodler):
    str = f'<input type="text" name="{key}" value="{valueLabel}" class="placeholder-input" placeholder="{placeHodler}" required>\n'
    return str

templates.env.globals["gatherGroupInformation"] = gatherGroupInformation