import streamlit as st
import pandas as pd

# Configuração da página para alta qualidade visual e responsividade
st.set_page_config(
    page_title="Yuan to Real",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)




# Inicializa a lista de produtos no session_state para manter os dados ao recarregar
if 'lista_produtos' not in st.session_state:
    st.session_state.lista_produtos = []
if 'valor_conversao_yuan' and 'valor_conversao_dolar' not in st.session_state:
    st.session_state.mostrar_form = True
    st.session_state.valor_conversao_yuan = 0.0
    st.session_state.valor_conversao_dolar = 0.0
if 'frete' not in st.session_state:
    st.session_state.frete = 0.0
    st.session_state.taxa_inclusa = False
    st.session_state.mostrar_frete = True

# Aplicação de estilo CSS customizado e moderno (Gradientes e Fontes)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    /* Configuração de Fonte Global */
    .stApp {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Estilização do Título Principal com Gradiente */
    .app-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #4F46E5, #EC4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.1rem;
    }
    
    .app-subtitle {
        font-size: 1.1rem;
        color: #6B7280;
        margin-bottom: 1.5rem;
    }
    
    /* Customização dos botões e contêineres */
    div.stButton > button {
        border-radius: 8px;
        transition: all 0.2s ease-in-out;
    }
    
    div.stButton > button:hover {
        transform: scale(1.02);
    }
    
    /* Ajustes para modo escuro */
    @media (prefers-color-scheme: dark) {
        .app-subtitle {
            color: #9CA3AF;
        }
    }
</style>
""", unsafe_allow_html=True)

# Layout do cabeçalho do app
col_title, col_logo = st.columns([6, 1])
with col_title:
    st.markdown('<h1 class="app-title">🛍️ Calculadora Yuan</h1>', unsafe_allow_html=True)

# Divisão de colunas principal: Cadastro no lado esquerdo, visualização no lado direito
col_input, col_display = st.columns([2, 3])

with col_input:
    if st.session_state.mostrar_form:
        st.subheader("💵 Conversão")
        with st.form("cadastro_conversao", clear_on_submit=True):
            valor_conversao_yuan = st.number_input("Valor da Conversão (Yuan)", min_value=0.0, step=0.01, key="form_conversao_yuan")
            valor_conversao_dolar = st.number_input("Valor da Conversão (Dólar)", min_value=0.0, step=0.01, key="form_conversao_dolar")
            submitted = st.form_submit_button("Adicionar Conversão")
            if submitted:
                if valor_conversao_yuan == 0 or valor_conversao_dolar == 0:
                    st.error("Por favor, insira valores válidos para a conversão!")
                else:
                    st.session_state.valor_conversao_yuan = valor_conversao_yuan
                    st.session_state.valor_conversao_dolar = valor_conversao_dolar
                    st.success(f"Conversão adicionada com sucesso!")
                    st.session_state.mostrar_form = False
                    st.rerun()
    else:
        st.subheader("💵 Conversão")            
        st.text(f"Conversão atual: {st.session_state.valor_conversao_yuan} Yuans")
        st.text(f"Conversão atual: {st.session_state.valor_conversao_dolar} Dólares")
        if st.button("Alterar Conversão"):
            st.session_state.mostrar_form = True
            st.rerun()

with col_input:
    if st.session_state.mostrar_frete:
        st.subheader("🛬Frete")
        with st.form("cadastro_frete", clear_on_submit=True):
            valor_frete = st.number_input("Valor do Frete (R$)", min_value=0.0, step=0.01, format="%.2f", key="form_frete")
            taxa_inclusa = st.checkbox("Taxa Inclusa", key="form_taxa_inclusa")
            submitted = st.form_submit_button("Adicionar Frete")
            if submitted:
                if valor_frete == 0:
                    st.error("Por favor, insira um valor válido para o frete!")
                else:
                    st.session_state.frete = valor_frete
                    st.session_state.taxa_inclusa = taxa_inclusa
                    st.success(f"Frete adicionado com sucesso!")
                    st.session_state.mostrar_frete = False
                    st.rerun()
    else:
        st.subheader("🛬 Frete")            
        st.text(f"Frete atual: {st.session_state.frete}")
        if st.button("Alterar Frete"):
            st.session_state.mostrar_frete = True
            st.rerun()

with col_display:
    st.subheader("➕ Adicionar Novo Item")
    
    # Formulário para cadastrar novos itens (limpa os inputs automaticamente após envio)
    with st.form("cadastro_produto", clear_on_submit=True):
        nome_produto = st.text_input("Nome do Produto", placeholder="Nome...", key="form_nome")
        
        col_price, col_qty, col_declarado = st.columns(3)
        with col_price:
            valor_produto = st.number_input("Valor Unitário (Yuan)", min_value=0, key="form_valor")
        with col_qty:
            qtd_produto = st.number_input("Quantidade", min_value=1, value=1, step=1, key="form_qtd")
        with col_declarado:
            valor_declarado = st.number_input("Valor Declarado (US$)", min_value=0, key="form_valor_declarado")
            
        
        submitted = st.form_submit_button("Adicionar à Lista")
        
        if submitted:
            if st.session_state.valor_conversao_yuan == 0 or st.session_state.valor_conversao_dolar == 0:
                st.error("Por favor, insira valores válidos para a conversão!")
            
            elif st.session_state.frete == 0:
                st.error("Por favor, insira um valor válido para o frete!")

            elif not nome_produto.strip() or valor_produto == 0 or valor_declarado == 0 or qtd_produto == 0:
                st.error("Por favor, digite o nome do produto e insira valores válidos para a conversão!")
            else:
                # Adiciona o produto na lista armazenada no estado da sessão
                st.session_state.lista_produtos.append({
                    "id": len(st.session_state.lista_produtos),
                    "nome": nome_produto.strip(),
                    "valor": valor_produto,
                    "quantidade": qtd_produto,
                    "total": valor_produto * qtd_produto,
                    "valor_declarado": valor_declarado,
                })
                st.success(f"'{nome_produto}' adicionado com sucesso!")
                st.rerun()



    
with col_display:
    st.subheader("📋 Lista de Itens")
    
    if not st.session_state.lista_produtos:
        st.info("Sua lista está vazia. Adicione produtos no formulário ao lado para começar!")
    else:
        # Cálculo dos totais agregados
        total_items = sum(item["quantidade"] for item in st.session_state.lista_produtos)
        total_value = sum(item["total"]/st.session_state.valor_conversao_yuan for item in st.session_state.lista_produtos)
        unique_items = len(st.session_state.lista_produtos)
        
        # Exibição das métricas com design elegante
        m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)
        with m_col1:
            st.metric("Total de Itens", f"{total_items} un")
        with m_col2:
            st.metric("Produtos Únicos", f"{unique_items}")
        with m_col3:
            if st.session_state.frete > 0:
                st.metric("Valor Total", f"R$ {total_value + st.session_state.frete :.2f}")
            else:
                st.metric("Valor Total", f"R$ {total_value :.2f}")
        with m_col4:
            declarado = sum(item["valor_declarado"] for item in st.session_state.lista_produtos)
            st.metric("Valor Declarado", f"R$ {declarado*st.session_state.valor_conversao_dolar:.2f}")
        with m_col5:
            if st.session_state.taxa_inclusa == True:
                st.metric("Imposto a Pagar", f"R$ {(declarado*st.session_state.valor_conversao_dolar + st.session_state.frete) * 0.92:.2f}")
            else:
                st.metric("Imposto a Pagar", f"R$ {declarado*st.session_state.valor_conversao_dolar *0.92:.2f}")
            
        st.markdown("---")
        
        # Filtro de busca na lista
        search_query = st.text_input("🔍 Buscar na lista", placeholder="Filtrar por nome do produto...", key="search")
        
        # Converter para DataFrame para facilitar o processamento e exibição
        df = pd.DataFrame(st.session_state.lista_produtos)
        
        if search_query:
            df_filtered = df[df["nome"].str.contains(search_query, case=False, na=False)]
        else:
            df_filtered = df
            
        # Lista dinâmica com botões de ação para remover itens individualmente
        for index, row in df_filtered.iterrows():
            # Localizar o índice real no session_state original
            actual_index = df.index[df['id'] == row['id']].tolist()[0]
            
            with st.container():
                col_info, col_price, col_decl, col_action = st.columns([5, 3, 2, 1])
                with col_info:
                    st.markdown(f"**{row['nome']}**")
                    st.caption(f"Qtd: {row['quantidade']}")
                with col_price:
                    st.markdown(f"**R$ {row['total']/ st.session_state.valor_conversao_yuan:.2f}**")
                    st.caption(f"Unidade: Yuan {row['valor']}")
                with col_decl:
                    st.text("Valor Declarado")
                    st.markdown(f"**US$ {row['valor_declarado']:.2f}**")
                with col_action:
                    # Botão para deletar o item atual
                    if st.button("🗑️", key=f"del_{row['id']}", help="Remover este item"):
                        st.session_state.lista_produtos.pop(actual_index)
                        # Reindexa os IDs remanescentes para evitar colisões
                        for idx, item in enumerate(st.session_state.lista_produtos):
                            item['id'] = idx
                        st.success(f"Item removido!")
                        st.rerun()
                st.markdown("<hr style='margin: 0.5rem 0;' />", unsafe_allow_html=True)
                
        # Ações de rodapé da lista
        st.markdown("<br>", unsafe_allow_html=True)
        col_clear, col_csv = st.columns([1, 1])
        with col_clear:
            if st.button("🔴 Limpar Lista Completa", key="clear_all", use_container_width=True):
                st.session_state.lista_produtos = []
                st.success("Lista limpa com sucesso!")
                st.rerun()
        with col_csv:
            if st.session_state.lista_produtos:
                csv_df = pd.DataFrame(st.session_state.lista_produtos)[["nome", "valor", "quantidade", "total"]]
                csv_data = csv_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Exportar para Excel/CSV",
                    data=csv_data,
                    file_name="lista_de_compras.csv",
                    mime="text/csv",
                    use_container_width=True,
                    key="export_csv"
                )
