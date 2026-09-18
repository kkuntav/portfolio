import pandas # type: ignore
import sqlite3
from openai import OpenAI # type: ignore
import os
import time
import re

OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY")


class Dabid:
    def __init__(self, file: str, lista: list[str]) -> None:
        self.file = file
        self.lista = lista
        self.tables = {}


    def buildDB(self) -> None:
        for i in self.lista:
            self.tables[i] = pandas.read_excel(self.file, sheet_name=i)


    def buildSQL(self) -> None:
        conn = sqlite3.connect("dabid/data/database.db")
        for name, tabla in self.tables.items():
            tabla.to_sql(name, conn, if_exists="replace", index=False)


    def getSchemas(self) -> list[str]:
        result = []
        for name, tabla in self.tables.items():
            aux = f"Table {name}("
            for i in tabla.columns:
                aux += f"{i} "
                match str(tabla[i].dtype):
                    case "object":
                        aux += "TEXT, "
                    case "int64":
                        aux += "INTEGER, "
                    case "float64":
                        aux += "REAL, "
                    case "bool":
                        aux += "BOOLEAN, "
                    case "datetime64[ns]":
                        aux += "TIMESTAMP, "
                    case _:
                        aux += "TEXT, "
            # Quitar coma final para formato
            aux = aux[:len(aux) - 2] + ")\n"
            result.append(aux)
        return result
            
    
    def askModel(self, query: str) -> str:
        client = OpenAI(api_key=OPENAI_API_KEY)
        schema = ""
        for i in self.getSchemas():
            schema += i + "\n"

        instructions = f"""
        You are an SQLite query generator.

        Your task is to convert the user's question into a valid SQL query using ONLY the tables and columns provided in the database schema.

        DATABASE SCHEMA:
        {schema}

        RULES:
        - Generate ONLY the SQL query. Do not provide explanations, comments, markdown, or any other text.
        - Use ONLY tables and columns that exist in the provided schema.
        - Do not invent table names or column names.
        - Use the exact table and column names provided in the schema.
        - The query must answer the user's question as accurately as possible.
        - If the question requires information from multiple tables, use the appropriate JOIN conditions based on the available columns.
        - Do not modify, delete, insert, update, or create any data.
        - Generate a read-only SELECT query.
        - Do not use SELECT * unless it is necessary to answer the question.
        - Return a single SQLite query.
        - If the question cannot be answered using the provided schema, return:
        SELECT 'Unable to answer the question using the provided database schema.' AS error;
        """

        prompt = f"""
        User Question: {query}
        """

        response = client.responses.create(
            model="gpt-5-mini",
            instructions=instructions,
            input=prompt
        )

        return response.output_text
    
    
    def getDocumentation(self, query_sql: str) -> pandas.core.frame.DataFrame:
        conn = sqlite3.connect("database.db")
        result = pandas.read_sql_query(query_sql, conn)
        conn.close()
        return result

    
    def dataframe_to_html(self, df) -> str:
        html = '<table>'

        # Cabeceras
        html += '<thead>'
        html += '<tr>'

        for column in df.columns:
            html += f'<th>{column}</th>'

        html += '</tr>'
        html += '</thead>'

        # Filas
        html += '<tbody>'

        for _, row in df.iterrows():

            html += '<tr>'

            for column in df.columns:

                value = row[column]

                if pandas.isna(value):
                    value = ""

                html += f'<td>{value}</td>'

            html += '</tr>'

        html += '</tbody>'
        html += '</table>'

        return html
    

    def format_sql(self, sql: str) -> str:

        sql = sql.strip()

        # Normalizar espacios, pero conservando inicialmente los saltos
        sql = re.sub(r"[ \t]+", " ", sql)
        sql = re.sub(r"\n+", "\n", sql)

        # SELECT
        sql = re.sub(
            r"\bSELECT\s+",
            "SELECT\n    ",
            sql,
            flags=re.IGNORECASE
        )

        # FROM
        sql = re.sub(
            r"\s+\bFROM\s+",
            "\nFROM ",
            sql,
            flags=re.IGNORECASE
        )

        # JOIN
        sql = re.sub(
            r"\s+(LEFT OUTER JOIN|RIGHT OUTER JOIN|FULL OUTER JOIN|"
            r"LEFT JOIN|RIGHT JOIN|INNER JOIN|FULL JOIN|CROSS JOIN|JOIN)\s+",
            r"\n\1 ",
            sql,
            flags=re.IGNORECASE
        )

        # ON
        sql = re.sub(
            r"\s+\bON\s+",
            "\n    ON ",
            sql,
            flags=re.IGNORECASE
        )

        # WHERE
        sql = re.sub(
            r"\s+\bWHERE\s+",
            "\nWHERE ",
            sql,
            flags=re.IGNORECASE
        )

        # GROUP BY
        sql = re.sub(
            r"\s+\bGROUP BY\s+",
            "\nGROUP BY\n    ",
            sql,
            flags=re.IGNORECASE
        )

        # HAVING
        sql = re.sub(
            r"\s+\bHAVING\s+",
            "\nHAVING ",
            sql,
            flags=re.IGNORECASE
        )

        # ORDER BY
        sql = re.sub(
            r"\s+\bORDER BY\s+",
            "\nORDER BY\n    ",
            sql,
            flags=re.IGNORECASE
        )

        # LIMIT
        sql = re.sub(
            r"\s+\bLIMIT\s+",
            "\nLIMIT ",
            sql,
            flags=re.IGNORECASE
        )

        # AND / OR
        sql = re.sub(
            r"\s+\bAND\s+",
            "\n    AND ",
            sql,
            flags=re.IGNORECASE
        )

        sql = re.sub(
            r"\s+\bOR\s+",
            "\n    OR ",
            sql,
            flags=re.IGNORECASE
        )

        # UNION
        sql = re.sub(
            r"\s+\bUNION ALL\s+",
            "\nUNION ALL\n",
            sql,
            flags=re.IGNORECASE
        )

        sql = re.sub(
            r"\s+\bUNION\s+",
            "\nUNION\n",
            sql,
            flags=re.IGNORECASE
        )

        # Comas
        sql = re.sub(
            r",\s*",
            ",\n    ",
            sql
        )

        # Limpiar espacios antes de saltos
        sql = re.sub(
            r"[ \t]+\n",
            "\n",
            sql
        )

        # Evitar demasiados saltos
        sql = re.sub(
            r"\n{2,}",
            "\n",
            sql
        )

        return sql.strip()
    
        

def main(lista: list[str], query: str, file: str = "dabid/data/tables.xlsx") -> tuple[str, str, str]:
    tiempo = ""
    if query == "":
        return "no_query", "", ""
    start = time.perf_counter()
    dabid = Dabid(file, lista)
    dabid.buildDB()
    dabid.buildSQL()
    answer = dabid.askModel(query)
    tabla = dabid.getDocumentation(answer)
    tabla = dabid.dataframe_to_html(tabla)
    answer = dabid.format_sql(answer)
    tiempo = f"Total time {time.perf_counter() - start:.1f} ms"
    return tiempo, answer, tabla



if __name__ == "__main__":
    file = "tables.xlsx"
    # , "employee_data"
    tables = ["departments", "employees", "performance_reviews", "salaries"]
    query = "What is the department with the most \"Needs Improvement\" ratings in PerformanceScore?"
    main(tables, query, file)