from read_file import ReadFile
from convert_sql import ConvertSQL, sqlite3
from ai_api import API, csv
import pandas as pd # type: ignore


def main():
    # Tomar files y convertirlos en dict
    #files = input("Files: ")
    # files = ["./benchmarks/salaries.csv", "./benchmarks/departments.csv",
    #          "./benchmarks/employees.csv", "./benchmarks/performance_reviews.csv"]
    
    files = ["./work.xlsx"]
    
    database = ReadFile(files)
    dict_tables = database.get_database()
    # primera = {}
    # primera["aux"] = dict_tables["work_Vergangenheit"]
    
    
    
    # Hacer el archivo SQL con todas las tablas
    # dict_tables --> dict{table_name, list[str, value]}
    sql_instance = ConvertSQL(dict_tables)
    print("SQL file 'tables' created correctly!")
    
    # Mandar la request al modelo de api ia
    aux = {}
    for i, val in dict_tables.items():
        if i == "work_FC" or i == "work_Zukunft Rekrutierung etc." or i == "Vergangenheit":
            continue
        aux[i] = val
    api = API(aux, print_sample=False)
    
    
    
    
    # para saber qué se le está mandando al modelo    
    # print(api.system_prompt)
    

    
    client_query = input(f"What do you want to know?\n")
    query = api.process_query(client_query)
    
    if query[0] == '`':  # caso ```sql
        query = query[7:len(query) - 4]
    print("API Query:")
    print(query)
    
    # result = sql_instance.execute_query(query)
    conn = sqlite3.connect("tables.db")

    df = pd.read_sql_query(query, conn)
    
    def clean_id(x):
        try:
            return int(float(x))
        except:
            return x
        
    try: 
        df["Personalnummer"] = df["Personalnummer"].apply(clean_id)
    except:
        df["personalnummer"] = df["personalnummer"].apply(clean_id)
    
    
    # df.to_csv("result.csv", index=False, encoding="utf-8-sig")
    df.to_excel("final_second.xlsx", index=False)

if __name__ == "__main__":
    main()
    
    
    
    
    
#     WITH "alle_monate" AS (
#   SELECT
#     1 AS "monat_sort",
#     "juristische_einheit_label",
#     "personalnummer",
#     "nachname",
#     "vorname",
#     "mitarbeiterkreis_picklist_label",
#     "fte_x_100",
#     "tatigkeitsbereich_picklist_label",
#     "position_planstellenbezeichnung_label",
#     "kostenstelle_code_kostenstelle",
#     "kostenstelle_label",
#     "kostenstelle_code_kostenstelle2",
#     "kostenstelle_label3",
#     "abteilung_label",
#     "division_label",
#     "vorgesetzter"
#   FROM "work_Jan 2026"
#   UNION ALL
#   SELECT
#     2 AS "monat_sort",
#     "juristische_einheit_label",
#     "personalnummer",
#     "nachname",
#     "vorname",
#     "mitarbeiterkreis_picklist_label",
#     "fte_x_100",
#     "tatigkeitsbereich_picklist_label",
#     "position_planstellenbezeichnung_label",
#     "kostenstelle_code_kostenstelle",
#     "kostenstelle_label",
#     "kostenstelle_code_kostenstelle2",
#     "kostenstelle_label3",
#     "abteilung_label",
#     "division_label",
#     "vorgesetzter"
#   FROM "work_Feb 2026"
#   UNION ALL
#   SELECT
#     3 AS "monat_sort",
#     "juristische_einheit_label",
#     "personalnummer",
#     "nachname",
#     "vorname",
#     "mitarbeiterkreis_picklist_label",
#     "fte_x_100",
#     "tatigkeitsbereich_picklist_label",
#     "position_planstellenbezeichnung_label",
#     "kostenstelle_code_kostenstelle",
#     "kostenstelle_label",
#     "kostenstelle_code_kostenstelle2",
#     "kostenstelle_label3",
#     "abteilung_label",
#     "division_label",
#     "vorgesetzter"
#   FROM "work_Mar 2026"
#   UNION ALL
#   SELECT
#     4 AS "monat_sort",
#     "juristische_einheit_label",
#     "personalnummer",
#     "nachname",
#     "vorname",
#     "mitarbeiterkreis_picklist_label",
#     "fte_x_100",
#     "tatigkeitsbereich_picklist_label",
#     "position_planstellenbezeichnung_label",
#     "kostenstelle_code_kostenstelle",
#     "kostenstelle_label",
#     "kostenstelle_code_kostenstelle2",
#     "kostenstelle_label3",
#     "abteilung_label",
#     "division_label",
#     "vorgesetzter"
#   FROM "work_Apr 2026"
#   UNION ALL
#   SELECT
#     5 AS "monat_sort",
#     "juristische_einheit_label",
#     "personalnummer",
#     "nachname",
#     "vorname",
#     "mitarbeiterkreis_picklist_label",
#     "fte_x_100",
#     "tatigkeitsbereich_picklist_label",
#     "position_planstellenbezeichnung_label",
#     "kostenstelle_code_kostenstelle",
#     "kostenstelle_label",
#     "kostenstelle_code_kostenstelle2",
#     "kostenstelle_label3",
#     "abteilung_label",
#     "division_label",
#     "vorgesetzter"
#   FROM "work_Mai 2026"
#   UNION ALL
#   SELECT
#     6 AS "monat_sort",
#     "juristische_einheit_label",
#     "personalnummer",
#     "nachname",
#     "vorname",
#     "mitarbeiterkreis_picklist_label",
#     "fte_x_100",
#     "tatigkeitsbereich_picklist_label",
#     "position_planstellenbezeichnung_label",
#     "kostenstelle_code_kostenstelle",
#     "kostenstelle_label",
#     "kostenstelle_code_kostenstelle2",
#     "kostenstelle_label3",
#     "abteilung_label",
#     "division_label",
#     "vorgesetzter"
#   FROM "work_Juni 2026"
#   UNION ALL
#   SELECT
#     7 AS "monat_sort",
#     "juristische_einheit_label",
#     "personalnummer",
#     "nachname",
#     "vorname",
#     "mitarbeiterkreis_picklist_label",
#     "fte_x_100",
#     "tatigkeitsbereich_picklist_label",
#     "position_planstellenbezeichnung_label",
#     "kostenstelle_code_kostenstelle",
#     "kostenstelle_label",
#     "kostenstelle_code_kostenstelle2",
#     "kostenstelle_label3",
#     "abteilung_label",
#     "division_label",
#     "vorgesetzter"
#   FROM "work_Juli 2026"
#   UNION ALL
#   SELECT
#     8 AS "monat_sort",
#     "juristische_einheit_label",
#     "personalnummer",
#     "nachname",
#     "vorname",
#     "mitarbeiterkreis_picklist_label",
#     "fte_x_100",
#     "tatigkeitsbereich_picklist_label",
#     "position_planstellenbezeichnung_label",
#     "kostenstelle_code_kostenstelle",
#     "kostenstelle_label",
#     "kostenstelle_code_kostenstelle2",
#     "kostenstelle_label3",
#     "abteilung_label",
#     "division_label",
#     "vorgesetzter"
#   FROM "work_August 2026"
#   UNION ALL
#   SELECT
#     9 AS "monat_sort",
#     "juristische_einheit_label",
#     "personalnummer",
#     "nachname",
#     "vorname",
#     "mitarbeiterkreis_picklist_label",
#     "fte_x_100",
#     "tatigkeitsbereich_picklist_label",
#     "position_planstellenbezeichnung_label",
#     "kostenstelle_code_kostenstelle",
#     "kostenstelle_label",
#     "kostenstelle_code_kostenstelle2",
#     "kostenstelle_label3",
#     "abteilung_label",
#     "division_label",
#     "vorgesetzter"
#   FROM "work_September 2026"
#   UNION ALL
#   SELECT
#     10 AS "monat_sort",
#     "juristische_einheit_label",
#     "personalnummer",
#     "nachname",
#     "vorname",
#     "mitarbeiterkreis_picklist_label",
#     "fte_x_100",
#     "tatigkeitsbereich_picklist_label",
#     "position_planstellenbezeichnung_label",
#     "kostenstelle_code_kostenstelle",
#     "kostenstelle_label",
#     "kostenstelle_code_kostenstelle2",
#     "kostenstelle_label3",
#     "abteilung_label",
#     "division_label",
#     "vorgesetzter"
#   FROM "work_Oktober 2026"
#   UNION ALL
#   SELECT
#     11 AS "monat_sort",
#     "juristische_einheit_label",
#     "personalnummer",
#     "nachname",
#     "vorname",
#     "mitarbeiterkreis_picklist_label",
#     "fte_x_100",
#     "tatigkeitsbereich_picklist_label",
#     "position_planstellenbezeichnung_label",
#     "kostenstelle_code_kostenstelle",
#     "kostenstelle_label",
#     "kostenstelle_code_kostenstelle2",
#     "kostenstelle_label3",
#     "abteilung_label",
#     "division_label",
#     "vorgesetzter"
#   FROM "work_November 2026"
#   UNION ALL
#   SELECT
#     12 AS "monat_sort",
#     "juristische_einheit_label",
#     "personalnummer",
#     "nachname",
#     "vorname",
#     "mitarbeiterkreis_picklist_label",
#     "fte_x_100",
#     "tatigkeitsbereich_picklist_label",
#     "position_planstellenbezeichnung_label",
#     "kostenstelle_code_kostenstelle",
#     "kostenstelle_label",
#     "kostenstelle_code_kostenstelle2",
#     "kostenstelle_label3",
#     "abteilung_label",
#     "division_label",
#     "vorgesetzter"
#   FROM "work_Dezember 2026"
# ),
# "mit_letztem_monat" AS (
#   SELECT
#     *,
#     MAX("monat_sort") OVER (PARTITION BY "personalnummer") AS "letzter_monat"
#   FROM "alle_monate"
# )
# SELECT
#   "juristische_einheit_label",
#   "personalnummer",
#   "nachname",
#   "vorname",
#   "mitarbeiterkreis_picklist_label",
#   MAX(CASE WHEN "monat_sort" = 1 THEN "fte_x_100" END) AS "fte_x_100_jan",
#   MAX(CASE WHEN "monat_sort" = 2 THEN "fte_x_100" END) AS "fte_x_100_feb",
#   MAX(CASE WHEN "monat_sort" = 3 THEN "fte_x_100" END) AS "fte_x_100_mar",
#   MAX(CASE WHEN "monat_sort" = 4 THEN "fte_x_100" END) AS "fte_x_100_apr",
#   MAX(CASE WHEN "monat_sort" = 5 THEN "fte_x_100" END) AS "fte_x_100_mai",
#   MAX(CASE WHEN "monat_sort" = 6 THEN "fte_x_100" END) AS "fte_x_100_juni",
#   MAX(CASE WHEN "monat_sort" = 7 THEN "fte_x_100" END) AS "fte_x_100_juli",
#   MAX(CASE WHEN "monat_sort" = 8 THEN "fte_x_100" END) AS "fte_x_100_august",
#   MAX(CASE WHEN "monat_sort" = 9 THEN "fte_x_100" END) AS "fte_x_100_september",
#   MAX(CASE WHEN "monat_sort" = 10 THEN "fte_x_100" END) AS "fte_x_100_oktober",
#   MAX(CASE WHEN "monat_sort" = 11 THEN "fte_x_100" END) AS "fte_x_100_november",
#   MAX(CASE WHEN "monat_sort" = 12 THEN "fte_x_100" END) AS "fte_x_100_dezember",
#   MAX(CASE WHEN "monat_sort" = "letzter_monat" THEN "tatigkeitsbereich_picklist_label" END) AS "tatigkeitsbereich_picklist_label",
#   MAX(CASE WHEN "monat_sort" = "letzter_monat" THEN "position_planstellenbezeichnung_label" END) AS "position_planstellenbezeichnung_label",
#   MAX(CASE WHEN "monat_sort" = "letzter_monat" THEN "kostenstelle_code_kostenstelle" END) AS "kostenstelle_code_kostenstelle",
#   MAX(CASE WHEN "monat_sort" = "letzter_monat" THEN "kostenstelle_label" END) AS "kostenstelle_label",
#   MAX(CASE WHEN "monat_sort" = "letzter_monat" THEN "kostenstelle_code_kostenstelle2" END) AS "kostenstelle_code_kostenstelle2",
#   MAX(CASE WHEN "monat_sort" = "letzter_monat" THEN "kostenstelle_label3" END) AS "kostenstelle_label3",
#   MAX(CASE WHEN "monat_sort" = "letzter_monat" THEN "abteilung_label" END) AS "abteilung_label",
#   MAX(CASE WHEN "monat_sort" = "letzter_monat" THEN "division_label" END) AS "division_label",
#   MAX(CASE WHEN "monat_sort" = "letzter_monat" THEN "vorgesetzter" END) AS "vorgesetzter"
# FROM "mit_letztem_monat"
# GROUP BY
#   "personalnummer",
#   "juristische_einheit_label",
#   "nachname",
#   "vorname",
#   "mitarbeiterkreis_picklist_label"
# ORDER BY "personalnummer";