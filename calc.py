import streamlit as st
import pandas as pd

# =====================================================
# CONFIGURAÇÃO DA PÁGINA
# =====================================================

st.set_page_config(
    page_title="Yuan to Real",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# SESSION STATE
# =====================================================

if 'lista_produtos' not in st.session_state:
    st.session_state.lista_produtos = []

if 'mostrar_form' not in st.session_state:
    st.session_state.mostrar_form = True

if 'valor_conversao_yuan' not in st.session_state:
    st.session_state.valor_conversao_yuan = 0.0

if 'valor_conversao_dolar' not in st.session_state:
    st.session_state.valor_conversao_dolar = 0.0

if 'frete' not in st.session_state:
    st.session_state.frete = 0.0

if 'taxa_inclusa' not in st.session_state:
    st.session_state.taxa_inclusa = False

if 'mostrar_frete' not in st.session_state:
    st.session_state.mostrar_frete = True

if 'modo_layout' not in st.session_state:
    st.session_state.modo_layout = "desktop"

# =====================================================
# SIDEBAR / RESPONSIVIDADE
# =====================================================

st.sidebar.markdown("## 🎨 Layout")

modo = st.sidebar.radio(
    "Escolha o modo:",
    ["desktop", "mobile"],
    index=0 if st.session_state.modo_layout == "desktop" else 1
)

st.session_state.modo_layout = modo

# =====================================================
# CSS CUSTOMIZADO
# =====================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
}

/* Título */

.app-title {
    font-size: 2.7rem;
    font-weight: 700;
    background: linear-gradient(135deg, #4F46E5, #EC4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
}

.app-subtitle {
    font-size: 1rem;
    color: #6B7280;
    margin-bottom: 1.5rem;
}

/* Botões */

div.stButton > button {
    border-radius: 12px;
    transition: all 0.2s ease;
    font-weight: 600;
    height: 45px;
}

div.stButton > button:hover {
    transform: scale(1.02);
}

/* Cards */

[data-testid="metric-container"] {
    border-radius: 15px;
    padding: 15px;
    background-color: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.05);
}

/* Inputs */

.stTextInput input,
.stNumberInput input {
    border-radius: 10px;
}

/* Mobile */

@media (max-width: 768px) {

.block-container {
    padding-top: 0.8rem !important;
    padding-bottom: 1rem !important;
}

/* Desktop */
@media (min-width: 769px) {
    .block-container {
        padding-left: 3rem !important;
        padding-right: 3rem !important;
        max-width: 1400px;
    }
}

/* Mobile */
@media (max-width: 768px) {
    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    .app-title {
        font-size: 2rem !important;
    }

    div.stButton > button {
        width: 100%;
    }
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# LAYOUT PRINCIPAL
# =====================================================

if modo == "mobile":
    col_input = st.container()
    col_display = st.container()

else:
    col_input, col_display = st.columns([2, 3])

# =====================================================
# CABEÇALHO
# =====================================================

st.markdown(
    '<h1 class="app-title">🛍️ Calculadora Yuan</h1>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="app-subtitle">Converta produtos importados facilmente</p>',
    unsafe_allow_html=True
)

# =====================================================
# COLUNA INPUT
# =====================================================

with col_input:

    # =========================================
    # CONVERSÃO
    # =========================================

    st.subheader("💵 Conversão")

    if st.session_state.mostrar_form:

        with st.form("cadastro_conversao", clear_on_submit=True):

            valor_conversao_yuan = st.number_input(
                "Valor da Conversão (Yuan)",
                min_value=0.0001,
                format="%.4f",
                step=0.0001
            )

            valor_conversao_dolar = st.number_input(
                "Valor da Conversão (Dólar)",
                min_value=0.0001,
                format="%.4f",
                step=0.0001
            )

            submitted = st.form_submit_button("Adicionar Conversão")

            if submitted:

                st.session_state.valor_conversao_yuan = valor_conversao_yuan
                st.session_state.valor_conversao_dolar = valor_conversao_dolar
                st.session_state.mostrar_form = False

                st.success("Conversão adicionada!")
                st.rerun()

    else:

        st.info(
            f"""
            Yuan: ¥ {st.session_state.valor_conversao_yuan}

            Dólar: $ {st.session_state.valor_conversao_dolar}
            """
        )

        if st.button("Alterar Conversão"):
            st.session_state.mostrar_form = True
            st.rerun()

    st.markdown("---")

    # =========================================
    # FRETE
    # =========================================

    st.subheader("🛬 Frete")

    if st.session_state.mostrar_frete:

        with st.form("cadastro_frete", clear_on_submit=True):

            valor_frete = st.number_input(
                "Valor do Frete (R$)",
                min_value=0.0,
                step=0.01,
                format="%.2f"
            )

            taxa_inclusa = st.checkbox("Taxa Inclusa")

            submitted = st.form_submit_button("Adicionar Frete")

            if submitted:

                st.session_state.frete = valor_frete
                st.session_state.taxa_inclusa = taxa_inclusa
                st.session_state.mostrar_frete = False

                st.success("Frete adicionado!")
                st.rerun()

    else:

        st.info(f"Frete atual: R$ {st.session_state.frete:.2f}")

        if st.button("Alterar Frete"):
            st.session_state.mostrar_frete = True
            st.rerun()

# =====================================================
# COLUNA DISPLAY
# =====================================================

with col_display:

    # =========================================
    # FORM PRODUTO
    # =========================================

    st.subheader("➕ Adicionar Novo Item")

    with st.form("cadastro_produto", clear_on_submit=True):

        nome_produto = st.text_input(
            "Nome do Produto",
            placeholder="Digite o nome..."
        )

        if modo == "mobile":
            col_price = st.container()
            col_qty = st.container()
            col_decl = st.container()
        else:
            col_price, col_qty, col_decl = st.columns(3)

        with col_price:
            valor_produto = st.number_input(
                "Valor Unitário (Yuan)",
                min_value=0.0
            )

        with col_qty:
            qtd_produto = st.number_input(
                "Quantidade",
                min_value=1,
                value=1,
                step=1
            )

        with col_decl:
            valor_declarado = st.number_input(
                "Valor Declarado (US$)",
                min_value=0.0
            )

        submitted = st.form_submit_button("Adicionar à Lista")

        if submitted:

            if (
                st.session_state.valor_conversao_yuan == 0 or
                st.session_state.valor_conversao_dolar == 0
            ):
                st.error("Configure a conversão primeiro!")

            elif st.session_state.frete == 0:
                st.error("Configure o frete!")

            elif (
                not nome_produto.strip()
                or valor_produto == 0
                or valor_declarado == 0
            ):
                st.error("Preencha todos os campos!")

            else:

                st.session_state.lista_produtos.append({
                    "id": len(st.session_state.lista_produtos),
                    "nome": nome_produto.strip(),
                    "valor": valor_produto,
                    "quantidade": qtd_produto,
                    "total": valor_produto * qtd_produto,
                    "valor_declarado": valor_declarado
                })

                st.success(f"{nome_produto} adicionado!")
                st.rerun()

    st.markdown("---")

    # =========================================
    # LISTA
    # =========================================

    st.subheader("📋 Lista de Itens")

    if not st.session_state.lista_produtos:

        st.info("Nenhum item adicionado.")

    else:

        total_items = sum(
            item["quantidade"]
            for item in st.session_state.lista_produtos
        )

        total_value = sum(
            item["total"] / st.session_state.valor_conversao_yuan
            for item in st.session_state.lista_produtos
        )

        unique_items = len(st.session_state.lista_produtos)

        declarado = sum(
            item["valor_declarado"]
            for item in st.session_state.lista_produtos
        )

        # =====================================
        # MÉTRICAS RESPONSIVAS
        # =====================================

        if modo == "mobile":

            m1, m2 = st.columns(2)
            m3, m4 = st.columns(2)

            with m1:
                st.metric("Itens", total_items)

            with m2:
                st.metric("Produtos", unique_items)

            with m3:
                st.metric(
                    "Total",
                    f"R$ {total_value + st.session_state.frete:.2f}"
                )

            with m4:
                st.metric(
                    "Declarado",
                    f"R$ {declarado * st.session_state.valor_conversao_dolar:.2f}"
                )

            imposto = (
                (declarado * st.session_state.valor_conversao_dolar)
                + st.session_state.frete
            ) * 0.92

            st.metric("Imposto", f"R$ {imposto:.2f}")

        else:

            m1, m2, m3, m4, m5 = st.columns(5)

            with m1:
                st.metric("Itens", total_items)

            with m2:
                st.metric("Produtos", unique_items)

            with m3:
                st.metric(
                    "Total",
                    f"R$ {total_value + st.session_state.frete:.2f}"
                )

            with m4:
                st.metric(
                    "Declarado",
                    f"R$ {declarado * st.session_state.valor_conversao_dolar:.2f}"
                )

            imposto = (
                (declarado * st.session_state.valor_conversao_dolar)
                + st.session_state.frete
            ) * 0.92

            with m5:
                st.metric("Imposto", f"R$ {imposto:.2f}")

        st.markdown("---")

        # =====================================
        # BUSCA
        # =====================================

        search_query = st.text_input(
            "🔍 Buscar Produto",
            placeholder="Digite para buscar..."
        )

        df = pd.DataFrame(st.session_state.lista_produtos)

        if search_query:
            df_filtered = df[
                df["nome"].str.contains(
                    search_query,
                    case=False,
                    na=False
                )
            ]
        else:
            df_filtered = df

        # =====================================
        # ITENS
        # =====================================

        for index, row in df_filtered.iterrows():

            actual_index = df.index[
                df['id'] == row['id']
            ].tolist()[0]

            with st.container():

                if modo == "mobile":

                    st.markdown(f"### {row['nome']}")

                    c1, c2 = st.columns(2)

                    with c1:
                        st.caption(f"Qtd: {row['quantidade']}")
                        st.write(
                            f"R$ {row['total'] / st.session_state.valor_conversao_yuan:.2f}"
                        )

                    with c2:
                        st.caption("Declarado")
                        st.write(f"US$ {row['valor_declarado']:.2f}")

                    if st.button(
                        "🗑️ Remover",
                        key=f"del_{row['id']}"
                    ):

                        st.session_state.lista_produtos.pop(actual_index)

                        for idx, item in enumerate(
                            st.session_state.lista_produtos
                        ):
                            item['id'] = idx

                        st.rerun()

                else:

                    col_info, col_price, col_decl, col_action = st.columns(
                        [5, 3, 2, 1]
                    )

                    with col_info:
                        st.markdown(f"**{row['nome']}**")
                        st.caption(f"Qtd: {row['quantidade']}")

                    with col_price:
                        st.markdown(
                            f"**R$ {row['total'] / st.session_state.valor_conversao_yuan:.2f}**"
                        )

                    with col_decl:
                        st.markdown(
                            f"**US$ {row['valor_declarado']:.2f}**"
                        )

                    with col_action:

                        if st.button(
                            "🗑️",
                            key=f"del_{row['id']}"
                        ):

                            st.session_state.lista_produtos.pop(actual_index)

                            for idx, item in enumerate(
                                st.session_state.lista_produtos
                            ):
                                item['id'] = idx

                            st.rerun()

                st.markdown("---")

        # =====================================
        # RODAPÉ
        # =====================================

        if st.button(
            "🔴 Limpar Lista Completa",
            use_container_width=True
        ):

            st.session_state.lista_produtos = []

            st.success("Lista limpa!")
            st.rerun()