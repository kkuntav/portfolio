"""
Project: Project Demo
File: ai_api.py
Author: Diego Vegas Acosta
Date: 30/03/26

Description:
----------------------------------------------------------------------------
This file contains the interaction with the openai API, embeddings and process
of classify sensitive columns (learning and mapping in json)

Main Features:
----------------------------------------------------------------------------
- OpenAI Key
- Embedding, centroids, sensitive columns
- SQL query process

Technologies Used:
----------------------------------------------------------------------------
- Python, JSON
- OpenAI API
- Embedding

Notes:
----------------------------------------------------------------------------
- Centroids' concepts are in ./resources/sensitive_columns.txt
- ./resources/sensitive_hash.txt detects if the file containing the concepts changes and in here it does the embeds again
- Billing coudl be stored 

Usage:
----------------------------------------------------------------------------
Import it as a module:
    from ai_api import API

Example:
----------------------------------------------------------------------------
# Example usage
if __name__ == "__main__":

"""


import openai  # type: ignore
import numpy as np  # type: ignore
import csv
import json
from datetime import datetime

from boundaries import COST_PER_1K_TOKENS, hash_changed, normalize


class API:
    system_prompt: str
    
    def __init__(self, db: dict[str, dict[str, list]], print_sample=False):
        openai.api_key = "api"
        # estudia y edita el json y devuelve el sample con tablas censuradas
        samples = {}
        for table_name, table in db.items():
            samples[table_name] = self.process_sample(table)
        
        if print_sample:
            for table_name, table in samples.items():
                print(f"Table name: {table_name}")
                for col, val in table.items():
                    print(col, val, "\n")
                print("\n")
        
        self.build_prompt(samples)
    
    
    def build_prompt(self, samples: dict[str, dict[str, list]]):
        context = ""
        for table_name, table in samples.items():
            context += f"Table: {table_name}\n"
            for col_name, values in table.items():
                if isinstance(values, list):
                    vals = ", ".join(map(str, values))
                else:
                    vals = values
                context += f"- {col_name}: {vals}\n"
            context += "\n"

        self.system_prompt = (
            f"You are an expert SQLite query generator. Generate exactly ONE valid SQLite query based on the user request."
            f"{context}"
            f"Rules:\n- Query has to be ONLY SQLITE\n- ALWAYS wrap column and table names in double quotes ("")\n- [HIDDEN] = valid column to use in query, values not shown for privacy\n- use only given columns\n- 1 SQLite query only"
        )
    

    def process_sample(self, db: dict[str, list], threshold=0.60) -> dict[str, list]:
        cols = [normalize(i) for i in db.keys()]
        no_normal_col = list(db.keys())

        path = "./resources/mapping.json"

        # cargar mapping
        with open(path, "r", encoding="utf-8") as f:
            mapping = json.load(f)

        # detectar nuevas columnas
        new_appears = [col for col in cols if col not in mapping]

        if new_appears:
            new_mapping = self.check_similarity(new_appears)
            mapping.update(new_mapping)

            # guardar mapping actualizado
            with open(path, "w", encoding="utf-8") as f:
                json.dump(mapping, f, indent=2)

        sample: dict[str, list] = {}

        for col, sql_col in zip(cols, no_normal_col):

            score = mapping[col]["score"]

            if score < threshold:

                # obtener valores únicos sin romper orden
                values = list(dict.fromkeys(db[sql_col]))

                # limpiar posibles NaN / None
                values = [v for v in values if v is not None and str(v).lower() != "nan"]

                if len(values) == 0:
                    sample[sql_col] = []
                    continue

                if len(values) == 1:
                    sample[sql_col] = values
                    continue

                muestra = values[:2]

                # si alguno es muy largo, solo usar uno
                if any(len(str(v)) > 9 for v in muestra):
                    sample[sql_col] = [muestra[0]]
                else:
                    sample[sql_col] = muestra

            else:
                sample[sql_col] = ["[HIDDEN]"]
                # alternativa:
                # f"Sensitive information --> best match: {mapping[col]['concept']}, score: {score:.5f}"

        return sample


    def process_query(self, mensaje: str) -> str:
        # Comprobar gastos
        path = "./resources/billing.json"
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # "tokens": 13.983,
            # "calls": 50,
            # "cost": 0.05
        if data["billing"]["calls"] > 80:
            return "EXCEDIDO NÚMERO DE CALLS --> TOTAL DE 60 HECHAS"
        if data["billing"]["cost"] > 1.0:
            return "EXCEDIDO COSTE DE API --> MAYOR DE 0.50€"
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": mensaje}
        ]

        respuesta = openai.chat.completions.create(
            model="gpt-5.4",  # gpt-5.4-mini  -- gpt-5.4
            messages=messages,
            temperature=0.0
        )
        
        usage = respuesta.usage
        coste = self.calculate_cost(respuesta)

        # Actualizar billing
        data["billing"]["calls"] += 1
        data["billing"]["tokens"] += usage.total_tokens
        data["billing"]["cost"] += coste

        # Actualizar historial
        new_entry = {
            "id": data["billing"]["calls"],  # también se puede usar contasor separado
            "timestamp": datetime.now().isoformat(),
            "prompt_tokens": usage.prompt_tokens,
            "completion_tokens": usage.completion_tokens,
            "total_tokens": usage.total_tokens,
            "cost": coste,
            "query": mensaje
        }

        # Añadir al historial
        data["historial"].append(new_entry)

        # Guardar
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return respuesta.choices[0].message.content


    def calculate_cost(self, respuesta):
        prompt_tokens = respuesta.usage.prompt_tokens
        completion_tokens = respuesta.usage.completion_tokens
        model = respuesta.model

        # precios por 1K tokens (input, output)
        PRICING = {
            "gpt-5.4": (0.0025, 0.015),
            "gpt-5.4-mini": (0.00075, 0.0045),
            "gpt-4.1": (0.0020, 0.0080),
            "gpt-4.1-mini": (0.0004, 0.0016),
            "gpt-4o": (0.0025, 0.0100),
        }

        # fallback por si el modelo no está definido exactamente
        def get_pricing(model_name):
            for key in PRICING:
                if key in model_name:
                    return PRICING[key]
            raise ValueError(f"Modelo no soportado: {model_name}")

        input_price, output_price = get_pricing(model)

        coste = (
            (prompt_tokens / 1000) * input_price +
            (completion_tokens / 1000) * output_price
        )

        return coste


    def check_similarity(self, columns_name: list[str], build=False):
        # build es para crear el embebido por primera vez
        if hash_changed() or build:
            centroids = self.centroids_from_file()
            # Guardar centroides
            np.savez("./resources/centroids.npz", **centroids)
        # Cargar centroides
        data = np.load("./resources/centroids.npz")
        centroids = {key: data[key] for key in data}  # cada key del dict = nombre del array
            
        
        columnas_embed = self.embed(columns_name)
        json_entry = {}
        for embedding, column in zip(columnas_embed, columns_name):
            mejor_similitud = -1
            mejor_match = None
            for concept in centroids.keys():
                similitud = self.cosine(embedding, centroids[concept])
                if similitud > mejor_similitud:
                    mejor_similitud = similitud
                    mejor_match = concept
            json_entry[column] = {
                "concept": mejor_match,
                "score": mejor_similitud,
            }
        return json_entry


    def cosine(self, a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


    def centroids_from_file(self):
        """
        Lee el arhivo de sensitive_columns
        y devuelve: {
            concept: centroid_vector
        }
        """
        # lectrua de file
        concepts = {}
        with open("./resources/sensitive_columns.txt", "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                concept = row["concept"]
                phrases = [p.strip() for p in row["phrases"].split(";")]
                concepts[concept] = phrases

        # creacion de centroides desde dict 
        centroids = {}
        for concept, phrases in concepts.items():
            vectors = self.embed(phrases)
            centroids[concept] = np.mean(vectors, axis=0)
        return centroids


    def embed(self, frases, know_cost=False):
        response = openai.embeddings.create(
            model="text-embedding-3-large",
            input=frases
        )
        # response.data = [
        #   embedding(frase1),
        #   embedding(frase2),
        #   embedding(frase3),
        # ]
        if know_cost:
            tokens = response.usage.total_tokens
            print("Tokens:", tokens)
            costo = COST_PER_1K_TOKENS
            cost = (tokens / 1000) * costo
            print(cost)
        vectores = np.array([d.embedding for d in response.data])
        return vectores



if __name__ == "__main__":
    api = API({}, "test")
    result = api.check_similarity("name")
    print(result)