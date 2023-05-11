import json
import pandas as pd
from typing import List
import sqlite3
import xml.etree.ElementTree as ET


class DataReaderWriter:

    ### FUNCTIONS TO READ DATA INTO DICTIONARIES ###
    def read_csv(self, filename: str) -> List[dict]:
        df = pd.read_csv(filename)
        df_dict = json.loads(df.to_json(orient='index'))

        return list(df_dict.values())

    def read_json(self, filename: str) -> List[dict]:
        f = open(filename)
        data = json.load(f)
        f.close()

        return data["data"]

    def read_database_table(self, db: str, table: str) -> List[dict]:
        connection = sqlite3.connect(db)
        df = pd.read_sql_query(("select * from " + table), connection)
        connection.close()

        df_dict = json.loads(df.to_json(orient='index'))

        return list(df_dict.values())

    def read_xml(self, filename: str) -> List[dict]:
        tree = ET.parse(filename)
        root = tree.getroot()

        data = []
        for d in root:
            temp_dict = {}
            for obj in d:
                temp_dict[obj.tag] = obj.text
            data.append(temp_dict)

        return data

    ### FUNCTIONS TO CREATE DATA FILES/TABLE FROM DICTIONARIES ###
    def create_csv(self, data: List[dict], filename: str):
        df = pd.DataFrame.from_records(data)
        df.to_csv(filename, index=False)
    
    def create_json(self, data: List[dict], filename: str):
        with open(filename, "w") as outfile:
            outfile.write(json.dumps({"data": data}, indent=4))
    
    def create_xml(self, data: List[dict], filename: str):
        xml_data = ET.Element("data")

        for obj in data:
            temp_obj = ET.SubElement(xml_data, 'obj')
            for key in obj:
                el = ET.SubElement(temp_obj, key)
                el.text = str(obj[key])

        xml_binary = ET.tostring(xml_data)
        with open(filename, "wb") as f:
            f.write(xml_binary)

    def create_database_table(self, data: List[dict], database: str, table: str):
        df = pd.DataFrame.from_records(data)

        connection = sqlite3.connect(database)
        cursor = connection.cursor()

        cols = ""
        q_marks = ""
        for col in list(df.columns.values):
            cols += col+" text,"
            q_marks += "?,"
        cols = cols[:-1]
        q_marks = q_marks[:-1]

        rows = df.values.tolist()
        
        cursor.execute("create table if not exists  "+table+"("+cols+")")
        cursor.executemany("insert into "+table+" values (" + q_marks + ")", rows)        
        connection.commit()
        
        connection.close()
