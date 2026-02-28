import yaml
import pandas as pd
from io import BytesIO

class dataFilter:
    def __init__(self ,subDocConfig):
        with open(subDocConfig, "r", encoding="utf-8") as f:
            self.filterConfig = yaml.safe_load(f)
        # Intiate usefull variable 
        self.objectCounter = {}
        self.filteredData = {}
        for sheet in self.filterConfig["DocumentList"]:
            self.objectCounter[sheet] = 0
            self.filteredData[sheet] = []

    def findCorrectSheet(self,value):
        for sheet in self.filterConfig["DocumentList"]:
            if str(value).strip() in list(map(str,self.filterConfig[sheet]["MaDSCon"])):
                return sheet
            else:
                continue
        return "NoFound"

    def filterData(self,dataFrame,outputLocation):
        # Convert dataframe into dictonary
        dataDict = dataFrame.to_dict(orient="records")
        # Process data
        for row in dataDict:
            sheet = self.findCorrectSheet(row[self.filterConfig["MaDSConTitle"]])
            if sheet != "NoFound":
                objectData = {}
                self.objectCounter[sheet] = self.objectCounter[sheet] + 1
                row["index"] = self.objectCounter[sheet]
                for column in self.filterConfig[sheet]["CotDuLieu"]:
                    data = self.filterConfig[column]["Template"].format(**row)
                    objectData[self.filterConfig[column]["TenCot"]] = data
                self.filteredData[sheet].append(objectData)
            else:
                continue
        # Save into excel file
        savedData = {}
        for sheet in  self.filteredData.keys():
            savedData[sheet] = pd.DataFrame(self.filteredData[sheet])
        with pd.ExcelWriter(outputLocation, engine="openpyxl") as writer:
            for sheetName, df in savedData.items():
                df.to_excel(writer, sheet_name=self.filterConfig[sheetName]["SheetTitle"], index=False)
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            for sheetName, df in savedData.items():
                df.to_excel(
                    writer,
                    sheet_name=self.filterConfig[sheetName]["SheetTitle"],
                    index=False
                )

        output.seek(0)
        return output
