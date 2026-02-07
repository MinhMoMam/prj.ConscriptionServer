from fastapi import FastAPI, Request, Form, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import myPackages.dataContainer as dc
from typing import Dict, Any
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import yaml
from fastapi import HTTPException


excelFile = "data/CƠ CẤU HỆ THỐNG.xlsx"
settingFile = "setting/labelConfig.yaml"
typedefFile = "setting/DataType.yaml"
adminDivFile = "setting/AdministrativeDivision.yaml"
dataKey = ["Thuongtruap","Namsinh","Hovaten"]
searchingKey = ["Thuongtruap","Namsinh","Hovaten"]
requiredData = ["Namsinh","Hovaten"]
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
    retVal = dataCon.updateDataFrame(data,requiredData)
    return Response(status_code=204)  # No Content

@app.post("/submit-military-data/")
    

def gatherInformation(key,question,valueLabel,placeHodler,dataType):
    btn = f'<button type="button" class="auto-btn">▼</button>'
    required = ""
    if key in requiredData:
        required = "required"
    if dataType == "string":
        str = f'\n<div class="info-item">{question}: \n<input type="text" name="{key}" value="{valueLabel}" class="placeholder-input line-full" placeholder="{placeHodler}" {required}>\n</div>'
    else:
        str = f'<div class="autocomplete" id="{key}" style="width:150px;">{question}: \n<input class="auto-input" type="text" name="{key}" value="{valueLabel}" placeholder="{placeHodler} {required}">{btn}\n</div>'
    return  str

templates.env.globals["gatherInformation"] = gatherInformation

def gatherGroupInformation(key,valueLabel,placeHodler,dataType):
    btn = f'<button type="button" class="auto-btn">▼</button>'
    required = ""
    if key in requiredData:
        required = "required"
    if dataType == "string":
        str = f'<input type="text" name="{key}" value="{valueLabel}" class="placeholder-input" placeholder="{placeHodler}" {required}>\n'
    else:
        str = f'<span class="autocomplete" id="{key}" style="width:150px;">\n<input class="auto-input"  type="text" name="{key}" value="{valueLabel}" placeholder="{placeHodler}" {required}>{btn}\n</span>'
    return str

templates.env.globals["gatherGroupInformation"] = gatherGroupInformation

def createOptionList():
    retStr = "<script>\n"
    # Load configration
    with open(typedefFile, "r", encoding="utf-8") as f:
        typeDef = yaml.safe_load(f)
    with open(adminDivFile, "r", encoding="utf-8") as f:
        tree = yaml.safe_load(f)
    retStr = retStr + "Communes = [];\n"
    provinceList = "const Provinces = ["
    for province in tree["Provinces"]:
        provinceList = provinceList + f'"{province}"' + ","
    retStr = retStr + provinceList[:-1] +"];\n"
    for type in typeDef["DataTypeList"]:
        startStr = "const " + type + " = ["
        if "date" in type:
            for i in range(int(typeDef[type][0]), int(typeDef[type][1])+1):
                startStr += f'"{i}"' +","
        else:
            for value in typeDef[type]:
                startStr += f'"{value}"' +","
        startStr = startStr[:-1] + "];\n"
        retStr = retStr + startStr
    retStr = retStr + "</script>"
    return retStr

templates.env.globals["createOptionList"] = createOptionList


def createOptionForLables(config):
    retStr = "<script>\n"
    # Normal Types
    for column in config["columnList"]:
        if config[column]["DataType"] == "string" or config[column]["DataType"] == "Communes":
            continue
        else:
            retStr = retStr + f'autocomplete(document.getElementById("{column}"), {config[column]["DataType"]})\n'
    # Depending Types
    provinceList = {}
    commnuceList = {}
    for column in config["columnList"]:
        if config[column]["DataType"] == "Communes":
            foundMatched = False
            for provCol,value in provinceList.items():
                if value["Object"] == config[column]["Object"] and value["Group"] == config[column]["Group"]:
                    provinceList.pop(provCol)
                    retStr = retStr + f'autocompleteWithDependency(document.getElementById("{column}"), document.getElementById("{provCol}").querySelector(".auto-input"),COMMUNE_BY_DISTRICT)\n'
                    foundMatched = True
                    break
            if not foundMatched:
                commnuceList[column] = config[column]
        elif config[column]["DataType"] == "Provinces":
            foundMatched = False
            for comCol,value in commnuceList.items():
                if value["Object"] == config[column]["Object"] and value["Group"] == config[column]["Group"]:
                    commnuceList.pop(comCol)
                    retStr = retStr + f'autocompleteWithDependency(document.getElementById("{comCol}"), document.getElementById("{column}").querySelector(".auto-input"),COMMUNE_BY_DISTRICT)\n'
                    foundMatched = True
                    break
            if not foundMatched:
                provinceList[column] = config[column]
        else:
            continue
    retStr = retStr + "</script>"
    return retStr

templates.env.globals["createOptionForLables"] = createOptionForLables

def createCommnuneByDistrict():
    retStr = "<script>\n"
    retStr = retStr + "COMMUNE_BY_DISTRICT = {\n"
    with open(adminDivFile, "r", encoding="utf-8") as f:
        tree = yaml.safe_load(f)
    for province in tree["Provinces"]:
        communeList = ""
        for commune in tree[province]:
            communeList = communeList + f'"{commune}"' + ","
        retStr = retStr + f'"{province}": [{communeList[:-1]}],'
    retStr = retStr[:-1] + "\n}\n"
    retStr = retStr + "</script>"
    return retStr

templates.env.globals["createCommnuneByDistrict"] = createCommnuneByDistrict