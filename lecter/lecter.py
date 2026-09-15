from openai import OpenAI # type: ignore
import re
import time
import math
import json
import os
import gzip

OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY")

class Lecter:
    def __init__(self, file: str) -> None:
        self.file = file
        self.database: dict[int, list[str]] = {}
        self.embeddings: list[float] = []

    def buildEmbeddings(self) -> None:
        client = OpenAI(api_key=OPENAI_API_KEY)
        size = 0
        chunks = [i for lista in self.database.values() for i in lista]
        while size < len(chunks):
            # Se harán llamadas para chunks de tamaño 50 al embeber
            sending = chunks[size:size + 50]
            response = client.embeddings.create(
                model="text-embedding-3-large",
                input=sending
            )
            size += 50
            # si ponemos self.database en dim=1 sabemos a qué página pertenece
            # si hacemos zip en un for y dividimos por tamaños
            self.embeddings.extend([item.embedding for item in response.data])
    
    
    def top_k_neighbours(self, embed_query: list[float], k=5) -> list[tuple[int, float, str]]:
        # Se devuelve la página y el chunk en texto desde database
        cos_result: list[tuple[int, float]] = []

        for index, i in enumerate(self.embeddings):
            cos_result.append((index, self.cosineSim(embed_query, i)))

        cos_result.sort(key=lambda x: x[1], reverse=True)
        top_k = cos_result[:k]
        plane_chunks = [small for big in self.database.values() for small in big]
        result = []
        aux = []
        for i in top_k:
            aux.append(plane_chunks[i[0]])
        for page, values in self.database.items():
            for val in values:
                if val in aux:
                    position = aux.index(val)
                    result.append((page, top_k[position][1], val))
        result.sort(key=lambda x: x[1], reverse=True)
        return result


    def cosineSim(self, tensor1: list[float], tensor2: list[float]) -> float:
        # Num producto escalar
        # Den producto de las norm
        dot_product = 0
        norm_a = 0
        norm_b = 0

        for i in range(len(tensor1)):
            dot_product += tensor1[i] * tensor2[i]
            norm_a += tensor1[i] ** 2
            norm_b += tensor2[i] ** 2

        norm_a = math.sqrt(norm_a)
        norm_b = math.sqrt(norm_b)

        return dot_product / (norm_a * norm_b)



    def askModel(self, query: str, result) -> str:
        context = ""

        for page, similarity, text in result:
            context += (
                f"[Page {page + 1} | Similarity: {similarity:.4f}]\n"
                f"{text}\n\n"
            )

        client = OpenAI(api_key=OPENAI_API_KEY)

        instructions =  """
        You are a strict RAG question-answering system.

        Answer the question using ONLY the retrieved context.

        Rules:
        - Give a clear and direct answer.
        - Write 2 to 4 short paragraphs.
        - Separate different ideas into different paragraphs.
        - Keep each paragraph concise and easy to read.
        - Explain the answer using information explicitly supported by the context.
        - Do not use outside knowledge.
        - Do not speculate or infer information that is not supported by the context.
        - Prefer the highest-ranked relevant passages.
        - If one passage directly answers the question, expand the answer
        using only the relevant details from that passage.
        - Do not add unrelated background information.
        - Only cite pages that directly support the answer.
        - If the context does not contain enough information, say so.
        - Do not use the following character "—" NEVER, redact on a more human way
        """

        prompt = f"""
        Retrieved context: {context}
        Question: {query}
        """

        response = client.responses.create(
            model="gpt-5-mini",
            instructions=instructions,
            input=prompt
        )

        return response.output_text


    def loadEmbeddings(self) -> None:
        filename = f"lecter/data/{self.file}"
        with gzip.open(filename, "rt", encoding="utf-8") as file:
            data = json.load(file)

        self.database = {
            int(page): chunks
            for page, chunks in data["database"].items()
        }

        self.embeddings = data["embeddings"]

        print(f"Datos cargados desde {filename}")




def main(document: str, query: str) -> tuple[str, str]:
    tiempo = ""
    if query == "":
        tiempo = "no_query"
        return (tiempo, "")
    file = ""
    match document:
        case "sherlock":
            file = "sherlock.json.gz"
        case "metamorphosis":
             file = "meta.json.gz"
    lecter = Lecter(file)
    start = time.perf_counter()
    lecter.loadEmbeddings()  # --> DESPUÉS DE HABER CONSTRUIDO LOS EMBEDDING

    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=query
    )
    embed_query = response.data[0].embedding
    start = time.perf_counter()
    result = lecter.top_k_neighbours(embed_query, k=5)
    start = time.perf_counter()
    answer = lecter.askModel(query, result)
    tiempo = f"Total time of processing was {time.perf_counter() - start:.1f} ms"
    return (tiempo, answer)


if __name__ == "__main__":
    main(document="bible", query="Is it God merciful or just powerful?")