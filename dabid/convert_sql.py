"""
Project: Project Demo
File: convert_sql.py
Author: Diego Vegas Acosta
Date: 30/03/26

Description:
----------------------------------------------------------------------------
This module is responsible for converting the ReadFile object to a SQL file

Main Features:
----------------------------------------------------------------------------
- Data extracting (from de ReadFile object)
- Data tranforming (to a SQL file with normalized columns)


Technologies Used:
----------------------------------------------------------------------------
- Python
- SQL (database standard)

Notes:
----------------------------------------------------------------------------
- python -> sql
- The database could be extended to a SPARQL triples on future

Usage:
----------------------------------------------------------------------------
Import it as a module:
    from convert_sql import ConvertSQL

Example:
----------------------------------------------------------------------------
# Example usage
if __name__ == "__main__":

"""

import sqlite3
import pandas as pd  # type: ignore

class ConvertSQL:
    database: dict[str, dict[str, list[str]]]
    db_file_name = "tables.db"
    
    
    def __init__(self, db: dict[str, dict[str, list[str]]]) -> None:
        self.database = db
        self.create_db()
        self.insert_data()


    def create_db(self) -> None:
        conn = sqlite3.connect(self.db_file_name)
        cursor = conn.cursor()

        for table_name, table in self.database.items():
            column_names = table.keys()

            cols_sql = ", ".join(f'{self.sql_safe(col)} TEXT' for col in column_names)
            
            #   ("""CREATE TABLE employees (
            #           emp_id TEXT,
            #           first_name TEXT,
            #           last_name TEXT,
            #           employee_status TEXT
            #       )""")
            
            # Crear tabla incluso si ya existe 

            cursor.execute(f'DROP TABLE IF EXISTS {self.sql_safe(table_name)}')

            query = f'CREATE TABLE {self.sql_safe(table_name)} ({cols_sql})'
            cursor.execute(query)

        conn.commit()
        conn.close()


    def insert_data(self) -> None:
        conn = sqlite3.connect(self.db_file_name)
        cursor = conn.cursor()

        for table_name, table in self.database.items():
            column_names = list(table.keys())
            
            # SQL Query
            # INSERT INTO employees (emp_id, first_name, last_name)
            # VALUES (?, ?, ?)
            
            #     ("""INSERT INTO employees VALUES (?, ?, ?, ?)""", (
            #       self.database["emp_id"][i],
            #       self.database["first_name"][i],
            #       self.database["last_name"][i],
            #       self.database["employee_status"][i]
            #      )
            #       )

            placeholders = ", ".join(["?"] * len(column_names))
            col_names = ", ".join(self.sql_safe(col) for col in column_names)

            query = f'INSERT INTO {self.sql_safe(table_name)} ({col_names}) VALUES ({placeholders})'

            num_rows = len(next(iter(table.values())))

            for i in range(num_rows):
                row = tuple(
                    None if pd.isna(table[col][i]) else table[col][i]
                    for col in column_names
                )

                cursor.execute(query, row)
                # self.database["emp_id"][i],
                # self.database["first_name"][i],
                # Se hace de forma horizonal
        conn.commit()
        conn.close()
        
    
    def execute_query(self, query: str):
        conn = sqlite3.connect(self.db_file_name)
        cursor = conn.cursor()

        try:
            cursor.execute(query)

            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]

            normalized_rows = [
                tuple(0 if cell is None else cell for cell in row)
                for row in rows
            ]

            return column_names, normalized_rows
        
        except Exception:
            print("Fallo en execute_query con la query")

        finally:
            conn.close()
    
    
    def sql_safe(self, name: str) -> str:
        return f'"{name}"'