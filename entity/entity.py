from entity.qgram_index import main as qgram


def main(query: str) -> str:
    result = qgram(query, 3)
    aux = ""
    for i in result[1]:
        aux += i
        aux += "<br><br>"
    return aux