"""
Project: Project Demo
File: read_file.py
Author: Diego Vegas Acosta
Date: 30/03/26

Description:
----------------------------------------------------------------------------
This module is responsible for reading, cleaning and normalizing HR data
from csv files.

Main Features:
----------------------------------------------------------------------------
- Data reading (extracting from csv files)
- Data cleaning (handling missing values, duplicates, etc.)
- Data normalization (standardizing formats, column names, etc.)

Technologies Used:
----------------------------------------------------------------------------
- Python

Notes:
----------------------------------------------------------------------------
- csv -> python
- Range of synonims on the mapping for columns could be extended
- Error detection for file not existing could be implemented
- Only csv as input supported, not excel yet
- Normalization range could be expanded (like dates)

Usage:
----------------------------------------------------------------------------
Import it as a module:
    from read_file import ReadFile

Example:
----------------------------------------------------------------------------
# Example usage
if __name__ == "__main__":
    db = ReadFile("file_name")  
    # it gives the normalized columns names with their content from the file

"""
from pathlib import Path
from datetime import datetime
import chardet  # type: ignore
import pandas as pd  # type: ignore
from boundaries import normalize



class ReadFile:
    def __init__(self, files: list[str]) -> None:
        self.database: dict[str, dict[str, list]] = {}
        self.read(files)


    def normalize_value(self, value: str):
        # Vacíos → None (NULL en SQLite)
        if value == "":
            return None

        # Intentar INT
        try:
            return int(value)
        except:
            pass

        # Intentar FLOAT
        try:
            return float(value)
        except:
            pass

        # Intentar DATE
        for fmt in ("%d-%b-%y", "%d-%m-%Y"):
            try:
                return datetime.strptime(value, fmt).strftime("%Y-%m-%d")
            except:
                pass

        return value.strip()
    
    
    def read(self, files: list[str]) -> None:
        for file in files:
            name = Path(file).stem

            sheets = pd.read_excel(file, sheet_name=None)

            for sheet_name, df in sheets.items():

                # Limpiar nombres de columnas
                df.columns = (
                    df.columns
                    .str.strip()
                    .str.replace("\n", " ", regex=False)
                )

                df.columns = [normalize(col, to_sql=True) for col in df.columns]

                # eliminar duplicadas SOLO en esta hoja
                df = df.loc[:, ~df.columns.duplicated()]

                # Normalizar valores
                df = df.map(
                    lambda x: self.normalize_value(str(x).strip()) if pd.notnull(x) else x
                )

                self.database[f"{name}_{sheet_name}"] = df.to_dict(orient="list")


    # def read(self, files: list[str]) -> None:
    #     for file in files:
    #         name = Path(file).stem            
    #         table = {}
    #         # utf-8-sig
    #         with open(file, "rb") as f:
    #             rawdata = f.read()
    #             # esta debería ser la salida del chardet
    #             # {'encoding': 'Windows-1250', 'confidence': 0.92}
    #         encod = chardet.detect(rawdata)
    #         with open(file, "r", encoding=encod["encoding"]) as archivo:
    #             table.clear()
    #             columns = archivo.readline().strip().split(",")
    #             columns = [col.strip() for col in columns]
    #             columns = [normalize(i, to_sql=True) for i in columns]
    #             for col in columns:
    #                 table[col] = []
                    

    #             for line in archivo:
    #                 data = line.strip().split(",")
    #                 data = [self.normalize_value(value.strip()) for value in data]
    #                 for i, j in zip(columns, data):
    #                     table[i].append(j)
    #         self.database[name] = table


    def get_database(self) -> dict[str, dict[str, list]]:
        return self.database


# if __name__ == "__main__":
#     db = ReadFile("employee_data.csv")
#     for i, j in zip(db.database.items(), db.get_sample().items()):
#         print(i[0], i[1][:2])
#         print(j[0], j[1][:2])
#         print()