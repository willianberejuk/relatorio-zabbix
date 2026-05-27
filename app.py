import streamlit as st
import pandas as pd

from gerador_pdf import gerar_pdf

# =====================================================
# CONFIGURAÇÃO DA PÁGINA
# =====================================================

st.set_page_config(
    page_title="Relatório Zabbix",
    layout="wide"
)

# =====================================================
# TÍTULO
# =====================================================

st.title("Relatório Operacional - Eventos Zabbix")

# =====================================================
# CLIENTE
# =====================================================

cliente = st.text_input(
    "Nome do cliente",
    placeholder="Ex: Chiquinho - Shopping Central"
)

# =====================================================
# UPLOAD CSV
# =====================================================

arquivo = st.file_uploader(
    "Selecione a planilha CSV exportada do Zabbix",
    type=["csv"]
)

# =====================================================
# PROCESSAMENTO
# =====================================================

if arquivo is not None:

    try:

        # =============================================
        # LEITURA CSV
        # =============================================

        df = pd.read_csv(
            arquivo,
            encoding="utf-8-sig",
            sep=","
        )

        st.success("Arquivo carregado com sucesso!")

        # =============================================
        # CONVERTE DATAS
        # =============================================

        df["Time"] = pd.to_datetime(
            df["Time"],
            errors="coerce"
        )

        # =============================================
        # TABELA ORIGINAL
        # =============================================

        st.subheader("Eventos encontrados")

        st.dataframe(df)

        # =============================================
        # AGRUPAMENTO DOS ALERTAS
        # =============================================

        resumo_df = (
            df.groupby("Problem")
            .agg(
                Quantidade=("Problem", "count"),
                Ultima_Ocorrencia=("Time", "max")
            )
            .reset_index()
        )

        # =============================================
        # FORMATA DATA
        # =============================================

        resumo_df["Ultima_Ocorrencia"] = resumo_df[
            "Ultima_Ocorrencia"
        ].dt.strftime("%d/%m/%Y %H:%M")

        # =============================================
        # ORDENA
        # =============================================

        resumo_df = resumo_df.sort_values(
            by="Quantidade",
            ascending=False
        )

        # =============================================
        # EXIBE RESUMO
        # =============================================

        st.subheader("Resumo Operacional")

        st.dataframe(resumo_df)

        # =============================================
        # HOST
        # =============================================

        host = df["Host"].iloc[0]

        # =============================================
        # TOTAL EVENTOS
        # =============================================

        total_eventos = len(df)

        # =============================================
        # RESUMO EXECUTIVO
        # =============================================

        principal_alerta = resumo_df.iloc[0]["Problem"]

        qtd_principal = resumo_df.iloc[0]["Quantidade"]

        resumo_texto = f"""
        Durante o período analisado foram identificados
        {total_eventos} eventos para o host {host}.

        O alerta com maior recorrência foi:

        • {principal_alerta}
        ({qtd_principal} ocorrências)
        """

        st.subheader("Resumo Executivo")

        st.info(resumo_texto)

        # =============================================
        # VALIDA CLIENTE
        # =============================================

        if not cliente:

            st.warning("Informe o nome do cliente.")
            st.stop()

        # =============================================
        # BOTÃO PDF
        # =============================================

        if st.button("Gerar PDF"):

            caminho_pdf = "relatorios/relatorio.pdf"

            gerar_pdf(
                caminho_pdf,
                cliente,
                host,
                total_eventos,
                resumo_df
            )

            st.success("PDF gerado com sucesso!")

            with open(caminho_pdf, "rb") as pdf_file:

                st.download_button(
                    label="Baixar PDF",
                    data=pdf_file,
                    file_name="relatorio.pdf",
                    mime="application/pdf"
                )

    except Exception as erro:

        st.error(f"Erro ao processar arquivo: {erro}")
