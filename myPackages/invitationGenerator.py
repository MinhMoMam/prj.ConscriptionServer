import pandas as pd
import docx
from docx.shared import Pt
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from spire.doc import Document
from spire.doc import FileFormat
from spire.doc import BookmarksNavigator
import numbers
import decimal
import numpy
import yaml

class wordFileGenerator:
    def __init__(self, generatorConfigPath, lableConfigPath):
        # Load configration
        with open(lableConfigPath, "r", encoding="utf-8") as f:
            self.lableConfig = yaml.safe_load(f)
        with open(generatorConfigPath, "r", encoding="utf-8") as f:
            self.generatorConfig = yaml.safe_load(f)
        # Create lable Dictionary
        for column in self.lableConfig["columnList"]:
            self.columnConverter[self.lableConfig["column"]["ColumnLabel"]] = column
        