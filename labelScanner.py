import pandas as pd
import unicodedata, re
from jinja2 import Environment,FileSystemLoader

class columnPaser:
    def __init__(self, columnTitle):
        self.Name = self.createName(columnTitle)
        self.Title = columnTitle.replace("\n", "\\n")
        self.Question = self.createQuestion(columnTitle)
        self.Object = self.createObject(columnTitle)
        self.Group = self.createGroup(columnTitle)
        self.DataType = self.createDataType(columnTitle)

    def createGroup(self,columnTitle):
        column = columnTitle.upper()
        column = column.replace(" ","")
        if "NGÀYSINH" in column or "THÁNGSINH" in column or "NĂMSINH" in column:
            return "date"
        if "HỌ" in column and "TÊN" in column:
            return "objectName"
        if "HỌC" in column or "ĐÀOTẠO" in column or "TỐTNGHIỆP" in column or "TRÌNHĐỘ" in column or "C1" in column or "C2" in column or "C3" in column:
            return "education"
        if ("XÃ" in column or "TỈNH/TP" in column or "ẤP" in column or "SỐ NHÀ" in column) and "CẤP" not in column:
            if "THƯỜNGTRÚ" in column:
                return "thuongTru"
            if "TẠMTRÚ" in column:
                return "tamTru"
        if "MÃ4DS" in column or "NỘIDUNGXẾPLOẠI" in column:
            return "hiden"
        return "other"

    def createDataType(self,columnTitle):
        column = columnTitle.upper()
        column = column.replace(" ","")
        if "XÃ".replace(" ","") in column:
            return "Communes"
        if "TỈNH/TP".replace(" ","") in column:
            return "Provinces"
        if "HỌC VẤN".replace(" ","") in column:
            return "HocVan"
        if "SỐNG/CHẾT".replace(" ","") in column:
            return "SongChet"
        if "TRÌNH ĐỘ".replace(" ","") in column:
            return "TrinhDoChuyenMon"
        if "DÂN TỘC".replace(" ","") in column:
            return "DanToc"
        if "TÔN GIAO".replace(" ","") in column:
            return "TonGiao"
        if "QUỐC TÍCH".replace(" ","") in column:
            return "QuocTich"
        if "THÀNH PHẦN".replace(" ","") in column:
            return "ThanhPhan"
        if "CÓ".replace(" ","") in column and ("CHƯA".replace(" ","") in column or "KHÔNG".replace(" ","") in column):
            return "CoKhong"
        if "NGÀY".replace(" ","") in column and "CẤP".replace(" ","") not in column:
            return "dateDay"
        if "THÁNG".replace(" ","") in column:
            return "dateMonth"
        if "NĂM".replace(" ","") in column:
            return "dateYear"
        return "string"

    def createObject(self,columnTitle):
        column = columnTitle.upper()
        if "CHA" in column:
            return "father"
        if "MẸ" in column: 
            return "mother"
        if "ACE" in column:
            return "sibling"
        if "VỢ" in column or "CHỒNG" in column:
            return "wife"
        else:
            return "personal"

    def createQuestion(self,columnTitle):
        columnTitle = columnTitle.replace("\n", "\\n")
        return columnTitle

    def createName(self,columnTitle):
        retStr = re.sub(r'[^a-zA-Z0-9]', '',unicodedata.normalize('NFD', columnTitle).encode('ascii', 'ignore').decode())
        retStr = retStr.capitalize()
        return retStr

databasePath = "data/CƠ CẤU HỆ THỐNG.xlsx"
templateFile = "internal/labelConfig.temp"
outputFile = "setting/labelConfig_temp.yaml"
headRow = 1


if __name__ == "__main__":
    df = pd.read_excel(databasePath)
    # Read row at index 3 (4th row in Excel, excluding header)
    headers = df.columns.tolist()
    columnList = []
    for header in headers:
        columnList.append(columnPaser(header))

    data = {"columns": columnList}
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template(templateFile)
    output = template.render(data)

    with open(outputFile, "w", encoding="utf-8") as f:
        f.write(output)
