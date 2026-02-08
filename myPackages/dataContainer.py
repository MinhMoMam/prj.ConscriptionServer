import pandas as pd
import numpy as np
import yaml
import os

class dataContainer:
    def __init__(self, execelFile, setting,keys,searchingKeys):
        # Load configration
        with open(setting, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)
        # Load excel file
        self.excelFile = execelFile;
        self.dataframe = pd.read_excel(execelFile, sheet_name=self.config["Sheet"])
        self.dataframe = self.dataframe
        self.dataframe = self.dataframe.apply(pd.to_numeric, errors="ignore")
        float_cols = self.dataframe.select_dtypes(include="float").columns
        self.dataframe[float_cols] = (self.dataframe[float_cols].replace([np.inf, -np.inf], pd.NA).round().astype("Int64"))
        self.keys = keys
        self.searchingFactors = self.createSearchFactor(searchingKeys)
        # Load database:
        self.loadAndCreateDataBase()

    def createSearchFactor(self,searchingKeys):
        retDict = {key: [] for key in searchingKeys}
        for index, row in self.dataframe.iterrows():
            for key in searchingKeys:
                val = str(row[self.config[key]["ColumnLabel"]])
                if val != None and  val != 'Nan' and  val != 'nan' and  val != 'NAN' and val != '<NA>':
                    try:
                        dataType = self.config[key]["DataType"]
                        if dataType == "string":
                            val = str(val)
                        elif dataType == "number":
                            val = str(int(float(val)))
                    except:
                        print("[ERROR]: " + key + " cannot be used as key")
                        raise
                if val not in retDict[key]:
                    retDict[key].append(val)
        for key in self.keys:
            retDict[key] = sorted(retDict[key])
        return retDict

    def loadAndCreateDataBase(self):
        folder_path = "Database"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        for index, row in self.dataframe.iterrows():
            folderName = folder_path + "/"
            for key in self.keys:
                val = str(row[self.config[key]["ColumnLabel"]]).title().replace(" ","")
                if val != None and val != 'Nan' and val != '<Na>':
                    try:
                        dataType = self.config[key]["DataType"]
                        if dataType == "string":
                            val = str(val)
                        elif dataType == "number":
                            val = str(int(float(val)))
                    except:
                        print("[ERROR]: " + key + " cannot be used as key")
                        raise
                else:
                    val = "Unknown"
                folderName = folderName + val + "_"
            folderName = folderName[:-1]
            if not os.path.exists(folderName):
                os.makedirs(folderName)
                print("[Infor]: Create new folder - " + folderName)

    def getRootParam(self):
        return self.searchingFactors
    
    def returnSearchResult(self, searchingParam):
        self.loadAndCreateDataBase()
        retList = []
        retDataFrame = self.dataframe
        emptySearchParam = True
        for key,value in searchingParam.items():
            if value != "":
                if self.config[key]["DataType"] == "number":
                    value = int(value)
                    target_dtype = "Int64"
                else:
                    value = str(value)
                    target_dtype = "string"
                retDataFrame = retDataFrame[retDataFrame[self.config[key]["ColumnLabel"]].astype(target_dtype) == value]
                emptySearchParam = False
        if not emptySearchParam:
            for index, row in retDataFrame.iterrows():
                retDict = {}
                for key in searchingParam.keys():
                    retDict[key] = row[self.config[key]["ColumnLabel"]]
                retList.append(retDict)
        finalRestDict = self.searchingFactors
        finalRestDict["foundObj"] = retList
        return finalRestDict
    
    def retObjDetailInformation(self, searchingParam):
        retDict = {}
        retDataFrame = self.dataframe
        for key,value in searchingParam.items():
            if self.config[key]["DataType"] == "number":
                value = int(value)
                target_dtype = "Int64"
            else:
                value = str(value)
                target_dtype = "string"
            if value != "":
                retDataFrame = retDataFrame[retDataFrame[self.config[key]["ColumnLabel"]].astype(target_dtype) == value]
        if len(retDataFrame) != 1:
            return {}
        else:
            for column in self.config["columnList"]:
                if self.config[column]["Group"] == "hiden":
                    continue
                value = retDataFrame.iloc[0][self.config[column]["ColumnLabel"]]
                if str(value) == "nan" or str(value) == "<NA>":
                    retDict[column] = ""
                else:
                    retDict[column] = value
        FinalRetDict = {}
        FinalRetDict["obj"] = retDict
        FinalRetDict["config"] = self.config
        return FinalRetDict


    def updateDataFrame(self,input,requiredData):
        mask = pd.Series(True, index=self.dataframe.index)
        for column in requiredData:
            if self.config[column]["DataType"] == "number":
                value = int(input[column])
                target_dtype = "Int64"
            else:
                value = str(input[column])
                target_dtype = "string"
            mask &= self.dataframe[self.config[column]["ColumnLabel"]].astype(target_dtype) == value

        idx = self.dataframe[mask].index.tolist()
        if len(idx) == 0:
            return "CanFound"

        try:
            for key,value in input.items():
                if key in self.config["columnList"] and value != "":
                    dtype = self.dataframe[self.config[key]["ColumnLabel"]].dtype
                    self.dataframe.loc[idx, self.config[key]["ColumnLabel"]] = dtype.type(value)
        except:
            return "TypeError"
        
        return "Success"
    
    def saveExcelFile(self):
        # beginningDataframe = pd.read_excel(self.excelFile, sheet_name=self.config["Sheet"])
        # coloredDataFrame = highlight_differences(self.dataframe,beginningDataframe)
        self.dataframe.to_excel(self.excelFile, sheet_name=self.config["Sheet"], index=False)
        return True
    
def highlight_differences(df1, df2, color="yellow"):
    if df1.shape != df2.shape:
        raise ValueError("DataFrames must have the same shape")

    def style_func(x):
        styles = pd.DataFrame("", index=df1.index, columns=df1.columns)

        for i in range(df1.shape[0]):          # rows
            for j in range(df1.shape[1]):      # cols
                try:
                    if df1.iat[i, j] != df2.iat[i, j] and df1.iat[i, j] != "" :
                        styles.iat[i, j] = f"background-color: {color}"
                except:
                    continue

        return styles

    return df1.style.apply(style_func, axis=None)