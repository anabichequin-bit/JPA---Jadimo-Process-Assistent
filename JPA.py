import streamlit as st
import pandas as pd
from io import BytesIO

# ============================================================
# CONFIGURAÇÕES DA PÁGINA
# ============================================================
st.set_page_config(
    page_title="JPA Automação",
    layout="wide",
)

# ============================================================
# CSS DO NOVO TEMA BORDÔ + LAYOUT MODERNO
# ============================================================
st.markdown("""
<style>

body {
    background-color: #121212;
    color: #CFCFCF;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background-color: #1A1A1A;
    padding: 25px;
    width: 25% !important;
    border-right: 3px solid #7A0000; 
}

/* Título da sidebar */
.sidebar-title {
    font-size: 30px;
    font-weight: 300;
    font-family: "Calibri", sans-serif;
    color: #CFCFCF;
    padding-bottom: 10px;
}

/* Itens da sidebar */
.sidebar-item {
    font-size: 22px;
    color: #CFCFCF;
    margin: 14px 0 6px 0;
    font-family: "Calibri Light", sans-serif;
    cursor: pointer;
    transition: 0.2s ease;
}

/* Hover */
.sidebar-item:hover {
    color: white;
    margin-left: 6px;
}

/* Ativo */
.sidebar-item.selected {
    font-weight: 400;
    color: white;
    border-left: 3px solid #7A0000;
    padding-left: 10px;
}

/* ===== REGIÃO PRINCIPAL ===== */
.main-title {
    font-size: 42px;
    font-family: "Calibri Light", sans-serif;
    color: #7A0000;
    font-weight: 300;
    margin-bottom: 20px;
}

/* Botões gerais */
.stButton>button {
    background-color: #5A0000 !important;
    color: white !important;
    border-radius: 6px;
    font-size: 18px;
    height: 45px;
}

h1, h2, h3 {
    color: #CFCFCF !important;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# CONTROLE DE NAVEGAÇÃO
# ============================================================
query_params = st.query_params

if "tela" not in query_params:
    st.query_params["tela"] = "inicio"

tela = st.query_params["tela"]

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:

    st.markdown("<div class='sidebar-title'>Setores</div>", unsafe_allow_html=True)

    # RECEBIMENTO — link clicável sem botão invisível
    st.markdown("""
        <a href='?tela=recebimento'>
            <div class='sidebar-item selected'>Recebimento</div>
        </a>
    """, unsafe_allow_html=True)

    # NÃO CLICÁVEIS
    st.markdown("<div class='sidebar-item'>Expedição</div>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-item'>Jornada</div>", unsafe_allow_html=True)

# ============================================================
# TELA INICIAL
# ============================================================
if tela == "inicio":

    st.markdown("<div class='main-title'>JPA Automação</div>", unsafe_allow_html=True)
    st.write("Selecione um setor ao lado para continuar.")

# ============================================================
# TELA — RECEBIMENTO
# ============================================================
elif tela == "recebimento":

    st.markdown("<div class='main-title'>Automação de Menções – Recebimento</div>", unsafe_allow_html=True)

    st.write("Envie abaixo as planilhas para gerar automaticamente o modelo preenchido.")

    # ==================== UPLOAD ====================
    arquivo_bruto = st.file_uploader("Selecione a planilha BRUTA", type=["xlsx"])
    arquivo_modelo = st.file_uploader("Selecione a planilha MODELO (menções)", type=["xlsx"])

    # ==================== FUNÇÃO ====================
    def classificar_por_posicao(doc):
        resultado = {
            'Pedido Shipment': '',
            'Notas fiscais de peça': '',
            'Cte': '',
            'Notas fiscais de embalagem': ''
        }

        if len(doc) >= 1:
            resultado['Pedido Shipment'] = doc[0]
        if len(doc) >= 3:
            resultado['Notas fiscais de peça'] = doc[1] + '/' + doc[2]
        if len(doc) >= 5:
            resultado['Cte'] = doc[4]
        if len(doc) >= 6:
            resultado['Notas fiscais de embalagem'] = doc[5]

        return resultado

    # ==================== PROCESSAMENTO ====================
    if arquivo_bruto and arquivo_modelo:

        df_bruta = pd.read_excel(arquivo_bruto)
        df_bruta.columns = df_bruta.columns.str.strip()

        df_modelo = pd.read_excel(arquivo_modelo)

        coluna_codigos = "Malote"
        linhas_modelo = []

        for _, linha in df_bruta.iterrows():
            motorista = linha.get("Motorista", "")

            malote = linha.get(coluna_codigos)
            doc = [] if pd.isna(malote) else str(malote).split("/")

            dados = classificar_por_posicao(doc)

            linhas_modelo.append({
                "Motorista": motorista,
                "Pedido Shipment": dados["Pedido Shipment"],
                "Cte": dados["Cte"],
                "Notas fiscais de peça": dados["Notas fiscais de peça"],
                "Notas fiscais de embalagem": ""
            })

            if dados["Notas fiscais de embalagem"]:
                linhas_modelo.append({
                    "Motorista": motorista,
                    "Pedido Shipment": dados["Pedido Shipment"],
                    "Cte": dados["Cte"],
                    "Notas fiscais de peça": "",
                    "Notas fiscais de embalagem": dados["Notas fiscais de embalagem"]
                })

        df_final = pd.DataFrame(linhas_modelo)

        st.write("### ✔ Prévia do resultado")
        st.dataframe(df_final, height=350)

        # ==================== DOWNLOAD ====================
        buffer = BytesIO()
        df_final.to_excel(buffer, index=False)
        buffer.seek(0)

        st.download_button(
            label="⬇ Baixar planilha preenchida",
            data=buffer,
            file_name="planilha_preenchida.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
