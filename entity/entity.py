from entity.qgram_index import main as qgram


def main(query: str) -> tuple[str, str]:
    tiempo, resultados = qgram(query, 3)
    # El html inyectado debería tener un formato así:
    # <div class="result">
    #     <div class="result-info">
    #         <h3>Indiana</h3>
    #         <span class="score">225</span>
    #         <span class="qid">Q1415</span>
    #         <p>state of the United States of America</p>
    #     </div>
    # </div>

    # <div class="result">
    #     <div class="result-info">
    #         <h3>Indianapolis</h3>
    #         <span class="score">162</span>
    #         <span class="qid">Q6346</span>
    #         <p>capital city of the U.S. state of Indiana and the seat of Marion County</p>
    #     </div>

    #     <img src="http://commons.wikimedia.org/wiki/Special:FilePath/Downtown%20Indianapolis.jpg">
    # </div>
    div_result = "<div class=\"result\">\n"
    div_info = "<div class=\"result-info\">\n"
    div_end = "</div>\n"
    # [name], [score], [ped], [qid], [synon], [description], [foto]
    result = "<div class=\"results\">"
    for entidad in resultados:
        name, score, ped, qid, syn, description, foto = entidad
        result += div_result
        result += div_info

        result += f"<h3>{name}</h3>\n"
        if foto == "":
            result += "<img src=\"https://img.magnific.com/premium-vector/image-available-icon_268104-3618.jpg\">\n"
        else:
            result += f"<img src=\"{foto}\">\n"
        result += f"<p>{description}</p>\n"
        result += f"<span class=\"score\">{score}</span>\n"
        result += f"<span class=\"ped\">{ped}</span>\n"
        result += f"<span class=\"syn\">{syn}</span>\n"
        result += f"<span class=\"qid\">{qid}</span>\n"

        result += div_end
        result += div_end
    result += div_end
    return tiempo, result