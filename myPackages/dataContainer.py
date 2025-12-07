import pandas as pd
import yaml
import os

class dataContainer:
    def __init__(self, execelFile, setting):
        # Load configration
        with open(setting, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)
        # Load excel file
        self.dataframe = pd.read_excel(execelFile, sheet_name=self.config["Sheet"])
        self.dataframe = self.dataframe.astype(str)
        # Load database:
        self.loadAndCreateDataBase()

    def loadAndCreateDataBase(self):
        self.communeList = []
        self.yearOfBirthList = []
        self.objNameList = []
        folder_path = "Database"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        for index, row in self.dataframe.iterrows():
            Commune     = str(row[self.config["DCThT_Ap"]["ColumnLabel"]]).upper().replace("ẤP","").replace(" ","")
            yearOfBirth = str(row[self.config["NamSinh"]["ColumnLabel"]])
            objectName  = row[self.config["HoVaTen"]["ColumnLabel"]]
            objectName_ = objectName.replace(" ","_").replace(" ","_")
            folderName  = os.path.join(folder_path,(Commune + "_" + yearOfBirth + "_" + objectName_))
            if not os.path.exists(folderName):
                os.makedirs(folderName)
                print("[Infor]: Create new folder - " + folderName)
            if Commune not in self.communeList:
                self.communeList.append(Commune)
            if yearOfBirth not in self.yearOfBirthList:
                self.yearOfBirthList.append(yearOfBirth)
            if objectName not in self.objNameList:
                self.objNameList.append(objectName)
        self.communeList = sorted(self.communeList)
        self.yearOfBirthList = sorted(self.yearOfBirthList)
        self.objNameList = sorted(self.objNameList)

    def getRootParam(self):
        retDic = {}
        retDic["NameList"] = self.objNameList
        retDic["YearOfBirthList"] = self.yearOfBirthList
        retDic["CommuneList"] = self.communeList
        retDic["ObjectList"] = []
        return retDic
    
    def returnSearchResult(self, name, yearOfBirth, commune):
        self.loadAndCreateDataBase()
        retList = []
        retDataFrame = self.dataframe
        if not (name == "" and yearOfBirth == "" and commune == ""):
            if name != "":
                retDataFrame = retDataFrame[retDataFrame[self.config["HoVaTen"]["ColumnLabel"]] == name]
            if yearOfBirth != "":
                retDataFrame = retDataFrame[retDataFrame[self.config["NamSinh"]["ColumnLabel"]] == int(yearOfBirth)]
            if commune != "":
                retDataFrame = retDataFrame[retDataFrame[self.config["DCThT_Ap"]["ColumnLabel"]] == int(commune)]
            for index, row in retDataFrame.iterrows():
                retDict = {}
                retDict["name"]         = row[self.config["HoVaTen"]["ColumnLabel"]]
                retDict["yearOfBirth"]  = row[self.config["NamSinh"]["ColumnLabel"]]
                retDict["commune"]      = row[self.config["DCThT_Ap"]["ColumnLabel"]]
                retList.append(retDict)
        finalRestDict = {}
        finalRestDict["NameList"] = self.objNameList
        finalRestDict["YearOfBirthList"] = self.yearOfBirthList
        finalRestDict["CommuneList"] = self.communeList
        finalRestDict["ObjectList"] = retList
        return finalRestDict
    
    def retObjDetailInformation(self, name, yearOfBirth, commune):
        retDict = {}
        retDataFrame = self.dataframe
        if not (name == "" and yearOfBirth == "" and commune == ""):
            if name != "":
                dtype = self.dataframe[self.config["HoVaTen"]["ColumnLabel"]].dtype
                retDataFrame = retDataFrame[retDataFrame[self.config["HoVaTen"]["ColumnLabel"]] == dtype.type(name)]
            if yearOfBirth != "":
                dtype = self.dataframe[self.config["NamSinh"]["ColumnLabel"]].dtype
                retDataFrame = retDataFrame[retDataFrame[self.config["NamSinh"]["ColumnLabel"]] == dtype.type(yearOfBirth)]
            if commune != "":
                dtype = self.dataframe[self.config["DCThT_Ap"]["ColumnLabel"]].dtype
                print(self.config["DCThT_Ap"]["ColumnLabel"])
                retDataFrame = retDataFrame[retDataFrame[self.config["DCThT_Ap"]["ColumnLabel"]] == dtype.type(commune)]
        if len(retDataFrame) != 1:
            return {}
        else:
            for column in self.config["columnList"]:
                retDict[column] = retDataFrame.iloc[0][self.config[column]["ColumnLabel"]]
        return {"obj":retDict}


    def updateDataFrame(self,input):
        idx = self.dataframe.index[(self.dataframe[self.config["HoVaTen"]["ColumnLabel"]] == input["HoVaTen"])].tolist()
        for key,value in input.items():
            if key in self.config["columnList"]:
                dtype = self.dataframe[self.config[key]["ColumnLabel"]].dtype
                self.dataframe.loc[idx, self.config[key]["ColumnLabel"]] = dtype.type(value)
        return
