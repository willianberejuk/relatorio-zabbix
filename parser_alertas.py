from regras_alertas import REGRAS_ALERTAS


def analisar_alertas(df):

    resultados = []

    for _, linha in df.iterrows():

        problema = str(linha["Problem"])

        encontrou = False

        for chave, info in REGRAS_ALERTAS.items():

            if chave.lower() in problema.lower():

                resultados.append({
                    "host": linha["Host"],
                    "problema_original": problema,
                    "descricao": info["descricao"],
                    "causa": info["causa"]
                })

                encontrou = True
                break

        if not encontrou:

            resultados.append({
                "host": linha["Host"],
                "problema_original": problema,
                "descricao": "Alerta não mapeado",
                "causa": "Necessário análise manual"
            })

    return resultados