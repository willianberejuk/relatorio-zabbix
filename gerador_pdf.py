from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib import colors

from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)

import os

from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def gerar_pdf(
    caminho_pdf,
    cliente,
    host,
    total_eventos,
    resumo_df
):

    # =================================================
    # REGISTRA FONTE UTF-8
    # =================================================

    fonte_padrao = "Helvetica"
    fonte_caminho = os.path.join(
        os.path.dirname(__file__),
        "fontes",
        "DejaVuSans.ttf"
    )

    if os.path.exists(fonte_caminho):
        pdfmetrics.registerFont(
            TTFont(
                "DejaVu",
                fonte_caminho
            )
        )
        fonte_padrao = "DejaVu"

    # =================================================
    # DOCUMENTO
    # =================================================

    doc = SimpleDocTemplate(
        caminho_pdf,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )

    estilos = getSampleStyleSheet()

    elementos = []

    # =================================================
    # ESTILO TÍTULO
    # =================================================

    titulo_style = ParagraphStyle(
        "Titulo",
        parent=estilos["Heading1"],
        fontName=fonte_padrao,
        alignment=TA_CENTER,
        fontSize=20,
        leading=30,
        spaceAfter=30
    )

    # =================================================
    # ESTILO TEXTO
    # =================================================

    texto_style = ParagraphStyle(
        "Texto",
        parent=estilos["BodyText"],
        fontName=fonte_padrao,
        fontSize=11,
        leading=18
    )

    # =================================================
    # ESTILO SUBTÍTULO
    # =================================================

    subtitulo_style = ParagraphStyle(
        "Subtitulo",
        parent=estilos["Heading2"],
        fontName=fonte_padrao
    )

    # =================================================
    # ESTILO CÉLULAS TABELA
    # =================================================

    tabela_style = ParagraphStyle(
        "Tabela",
        parent=estilos["BodyText"],
        fontName=fonte_padrao,
        fontSize=8,
        leading=10
    )

    # =================================================
    # TÍTULO
    # =================================================

    titulo = Paragraph(
        "Relatório Operacional — Eventos Zabbix",
        titulo_style
    )

    elementos.append(titulo)

    # =================================================
    # CLIENTE / HOST
    # =================================================

    info = Paragraph(
        f"""
        <b>Cliente:</b> {cliente}<br/>
        <b>Host:</b> {host}<br/>
        <b>Total de eventos:</b> {total_eventos}
        """,
        texto_style
    )

    elementos.append(info)

    elementos.append(Spacer(1, 25))

    # =================================================
    # SUBTÍTULO
    # =================================================

    subtitulo = Paragraph(
        "<b>Resumo Operacional</b>",
        subtitulo_style
    )

    elementos.append(subtitulo)

    elementos.append(Spacer(1, 10))

    # =================================================
    # TABELA
    # =================================================

    dados_tabela = [[
        "Problem",
        "Quantidade",
        "Última ocorrência"
    ]]

    for _, linha in resumo_df.iterrows():

        problem_formatado = Paragraph(
            str(linha["Problem"]),
            tabela_style
        )

        dados_tabela.append([
            problem_formatado,
            str(linha["Quantidade"]),
            str(linha["Ultima_Ocorrencia"])
        ])

    tabela = Table(
        dados_tabela,
        colWidths=[360, 70, 110]
    )

    # =================================================
    # ESTILO TABELA
    # =================================================

    tabela.setStyle(TableStyle([

        # HEADER
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),

        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),

        ("FONTNAME", (0, 0), (-1, 0), fonte_padrao),

        ("FONTNAME", (0, 1), (-1, -1), fonte_padrao),

        ("FONTSIZE", (0, 0), (-1, -1), 9),

        # GRID
        ("GRID", (0, 0), (-1, -1), 1, colors.black),

        # ESPAÇAMENTO
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),

        ("TOPPADDING", (0, 0), (-1, 0), 8),

        ("BOTTOMPADDING", (0, 1), (-1, -1), 6),

        ("TOPPADDING", (0, 1), (-1, -1), 6),

        # ALINHAMENTO
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),

        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))

    elementos.append(tabela)

    caminho_diretorio = os.path.dirname(caminho_pdf)
    if caminho_diretorio:
        os.makedirs(caminho_diretorio, exist_ok=True)

    # =================================================
    # GERA PDF
    # =================================================

    doc.build(elementos)