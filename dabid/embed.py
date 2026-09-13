from openai import OpenAI
import numpy as np

client = OpenAI(api_key="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")


# Precio aproximado (verifica en tu dashboard)
COST_PER_1K_TOKENS = 0.00002  # text-embedding-3-small (aprox)

total_tokens_global = 0


def embed(text):
    global total_tokens_global

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    emb = np.array(response.data[0].embedding)

    tokens = response.usage.total_tokens
    total_tokens_global += tokens

    return emb


def cosine(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def comparar_con_lista(palabra, lista, threshold=0.5):
    global total_tokens_global

    emb_palabra = embed(palabra)

    mejor_sim = -1
    mejor_match = None

    for item in lista:
        emb_item = embed(item)
        sim = cosine(emb_palabra, emb_item)

        if sim > mejor_sim:
            mejor_sim = sim
            mejor_match = item

    return {
        "match": mejor_match,
        "similitud": mejor_sim,
        "tokens_usados": total_tokens_global,
        "coste_usd": f"{(total_tokens_global / 1000 * COST_PER_1K_TOKENS):.10f}"
    }


# ---------------- EJEMPLO ----------------

lista = ["name", "first name", "full name", "email", "address"]

result = comparar_con_lista("BusinessUnit", lista)

print(result)