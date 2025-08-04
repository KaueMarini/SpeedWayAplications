import streamlit as st
import pandas as pd
import re

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Dashboard de Análise de Grid",
    page_icon="🎯",
    layout="wide"
)
st.markdown("""
    <style>
    /* Importa fonte Inter */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #f4f4f8;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 1.5rem;
        padding-right: 1.5rem;
    }

    /* Containers com sombra e borda arredondada */
    div[data-testid="stContainer"] {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 2rem;
    }

    /* Botões modernos */
    div.stButton > button {
        background-color: #6f42c1;
        color: white;
        font-weight: 600;
        border-radius: 10px;
        padding: 0.75em 1.5em;
        transition: all 0.3s ease;
        border: none;
    }
    div.stButton > button:hover {
        background-color: #5a379d;
        transform: scale(1.02);
    }

    /* Ajustes para barra lateral */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e0e0e0;
    }

    /* Tooltip cursor */
    .styled-table td[title] {
        cursor: help;
    }

    /* Suporte a modo escuro automático */
    @media (prefers-color-scheme: dark) {
        html, body {
            background-color: #18191a !important;
            color: #f0f2f6;
        }
        .block-container {
            background-color: #1e1e1e;
        }
        div[data-testid="stContainer"] {
            background-color: #252526;
            box-shadow: none;
        }
        .styled-table thead tr {
            background-color: #3a3a3a !important;
        }
        .styled-table tbody tr:nth-of-type(even) {
            background-color: #2f2f2f !important;
        }
    }
    </style>
""", unsafe_allow_html=True)
st.markdown("""
    <style>
    /* Remove completamente a barra lateral */
    [data-testid="stSidebar"], section[data-testid="stSidebar"] {
        display: none !important;
    }

    /* Expande o conteúdo principal para ocupar o espaço total */
    .main .block-container {
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 100% !important;
    }

    /* Remove também o botão de recolher a sidebar */
    button[title="Toggle sidebar"] {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)
# --- FUNÇÕES DE LÓGICA ---
def limpar_e_organizar_dados(texto_colado):
    if not texto_colado: return []
    linhas = texto_colado.strip().split('\n')
    if len(linhas) < 3: return []
    linhas_de_dados = linhas[1:-1]
    grid_final = []
    NUM_COLUNAS_ESPERADO = 20
    for linha in linhas_de_dados:
        partes = linha.split()
        if not partes: continue
        dados_uteis = partes[1:-1]
        while len(dados_uteis) < NUM_COLUNAS_ESPERADO: dados_uteis.append('')
        grid_final.append(dados_uteis[:NUM_COLUNAS_ESPERADO])
    return grid_final

def completar_resultado_corrida(corrida_str):
    if not corrida_str or '-' not in corrida_str: return corrida_str
    pilotos_presentes = set(corrida_str.split('-'))
    if len(pilotos_presentes) == 3:
        todos_pilotos = {'1', '2', '3', '4'}
        try:
            piloto_faltando = list(todos_pilotos - pilotos_presentes)[0]
            return f"{corrida_str}-{piloto_faltando}"
        except IndexError: return corrida_str
    return corrida_str

def analisar_grid_continuo(dados_da_grade):
    lista_unica_corridas = [corrida for linha in dados_da_grade for corrida in linha if corrida and '-' in corrida]
    corridas_completas = [completar_resultado_corrida(c) for c in lista_unica_corridas]
    if len(corridas_completas) < 2: return [], [], []
    
    labels_continuos, tooltips_continuos = [], []
    for i in range(1, len(corridas_completas)):
        corrida_anterior_str, corrida_atual_str = corridas_completas[i-1], corridas_completas[i]
        anterior, atual = corrida_anterior_str.split("-"), corrida_atual_str.split("-")
        vencedor_atual = atual[0]
        label, tooltip, p1, p2 = "", "", False, False

        # Lógica de verificação P1/P2
        if len(anterior) > 1 and (vencedor_atual == anterior[0]): p1 = True
        elif len(anterior) > 3 and (vencedor_atual == anterior[3]): p1 = True
        elif len(anterior) > 2 and (vencedor_atual == anterior[1]): p2 = True
        elif len(anterior) > 2 and (vencedor_atual == anterior[2]): p2 = True
        
        # --- MUDANÇA NO TOOLTIP APLICADA AQUI ---
        if p1:
            label = "P1"
            tooltip = f"P1 (Corrida Atual: {corrida_atual_str})"
        elif p2:
            label = "P2"
            tooltip = f"P2 (Corrida Atual: {corrida_atual_str})"
            
        labels_continuos.append(label); tooltips_continuos.append(tooltip)
        
    return corridas_completas, labels_continuos, tooltips_continuos

def reconstruir_grid(dados_da_grade, labels, tooltips):
    num_rows, num_cols = len(dados_da_grade), len(dados_da_grade[0])
    grade_labels = [['' for _ in range(num_cols)] for _ in range(num_rows)]
    grade_tooltips = [['' for _ in range(num_cols)] for _ in range(num_rows)]
    
    corrida_idx = 0
    label_idx = 0
    
    for r in range(num_rows):
        for c in range(num_cols):
            if dados_da_grade[r][c] and '-' in dados_da_grade[r][c]:
                if corrida_idx > 0 and label_idx < len(labels):
                    grade_labels[r][c] = labels[label_idx]
                    grade_tooltips[r][c] = tooltips[label_idx]
                    label_idx += 1
                else:
                    grade_labels[r][c] = '-'
                    grade_tooltips[r][c] = 'Primeira corrida, sem análise.'
                corrida_idx += 1
    return grade_labels, grade_tooltips

def estilizar_tabela(val):
    if val == 'P1': return 'background-color: #6f42c1; color: white; font-weight: bold;'
    elif val == 'P2': return 'background-color: #008F8C; color: white; font-weight: bold;'
    elif isinstance(val, (int, float)) and val > 0: return 'background-color: #ffc107; color: black; font-weight: bold;'
    else: return 'color: #6c757d;'

# --- Bloco de Estilo CSS ---
CSS_ESTILO_TABELA = """
<style>
    /* Novo container para controlar a rolagem da tabela */
    .table-container {
        overflow-x: auto; /* Cria a barra de rolagem horizontal apenas quando necessário */
        margin-bottom: 2rem; /* Espaçamento opcional */
        border: 1px solid #dddddd;
        border-radius: 10px;
    }

    .styled-table {
        border-collapse: collapse; margin: 0; /* Margin removida para ajustar ao container */
        font-size: 0.9em;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        width: 100%; /* A tabela tentará ocupar todo o espaço do container */
        box-shadow: none; /* Sombra removida pois o container pode ter a sua */
        border-radius: 10px; overflow: hidden;
    }
    .styled-table thead tr {
        background-color: #343a40; color: #ffffff; text-align: center;
        font-weight: bold;
    }
    .styled-table th, .styled-table td { padding: 12px 15px; text-align: center; }
    .styled-table tbody tr { border-bottom: 1px solid #dddddd; }
    .styled-table tbody tr:nth-of-type(even) { background-color: #f8f9fa; }
    .styled-table tbody tr:last-of-type { border-bottom: none; } /* Removida a borda inferior grossa */
    .styled-table td[title] { cursor: help; }
</style>
"""

# --- INÍCIO DA INTERFACE GRÁFICA ---

st.title("🎯 Analisador de Grid Preciso")
st.markdown("Uma ferramenta visual para identificar padrões **P1** e **P2**, com tooltips simplificados e análise contínua.")

with st.container(border=True):
    st.subheader("📋 Etapa 1: Insira os Dados da Grade")
    dados_colados = st.text_area(
        "Cole todo o texto da sua tabela aqui:", height=300,
        placeholder="H 1 4 7...\n17 4-3-1 2-1-4...\n16 1-3-2 3-4-1...\n(Cole seus dados aqui)",
        label_visibility="collapsed"
    )
    debug_mode = st.checkbox("Ativar Modo de Depuração para verificar a lógica")
    botao_analisar = st.button("✨ Analisar e Gerar Dashboard!", type="primary", use_container_width=True)

st.divider()

if botao_analisar:
    dados_da_grade = limpar_e_organizar_dados(dados_colados)
    if not dados_da_grade:
        st.warning("⚠️ Nenhum dado válido para análise.")
    else:
        corridas_completas, labels_continuos, tooltips_continuos = analisar_grid_continuo(dados_da_grade)
        grade_labels, grade_tooltips = reconstruir_grid(dados_da_grade, labels_continuos, tooltips_continuos)

        if debug_mode:
            with st.container(border=True):
                st.subheader("🕵️‍♂️ Modo de Depuração Ativado")
                df_debug = pd.DataFrame({
                    "Corrida Anterior": ["-"] + corridas_completas[:-1],
                    "Corrida Atual": corridas_completas,
                    "Resultado da Análise": ["-"] + labels_continuos
                })
                st.dataframe(df_debug, use_container_width=True)
                st.markdown("---")
        
        if grade_labels:
            # Determina os nomes das linhas a partir do texto colado
            linhas_texto = [l.split()[0] for l in dados_colados.strip().split('\n')[1:-1]]

            from collections import Counter
            contagem = Counter()
            nomes_das_linhas = []
            for l in linhas_texto:
                contagem[l] += 1
                label = f"L {l}"
                if contagem[l] > 1:
                    label += f" ({contagem[l]})"
                nomes_das_linhas.append(label)

            
            nomes_das_colunas_header = dados_colados.strip().split('\n')[0].split()[1:]
            
            num_cols_data = len(grade_labels[0])
            df_resultados = pd.DataFrame(grade_labels, index=nomes_das_linhas, columns=nomes_das_colunas_header[:num_cols_data])
            df_tooltips = pd.DataFrame(grade_tooltips, index=nomes_das_linhas, columns=nomes_das_colunas_header[:num_cols_data])
            df_originais = pd.DataFrame(grade_labels, index=nomes_das_linhas, columns=nomes_das_colunas_header[:num_cols_data])
            soma_p1_por_linha = (df_resultados == 'P1').sum(axis=1)
            soma_p2_por_linha = (df_resultados == 'P2').sum(axis=1)
            df_resultados['Σ P1'] = soma_p1_por_linha
            df_resultados['Σ P2'] = soma_p2_por_linha
            df_tooltips['Σ P1'] = 'Soma de P1 na linha'
            df_tooltips['Σ P2'] = 'Soma de P2 na linha'

            # --- CÁLCULO DA TABELA DE SEQUÊNCIAS MOVIDO PARA CIMA ---
            df_seq = df_resultados.iloc[:, :-2].copy()  # Remove Σ colunas
            df_seq_tooltip = df_seq.copy()

            for i in range(len(df_seq)):
                linha = df_seq.iloc[i].tolist()
                nova_linha = [''] * len(linha)
                nova_tooltips = [''] * len(linha)
                j = 0
                while j < len(linha) - 1:
                    atual = linha[j]
                    prox = linha[j + 1]
                    if atual in ['P1', 'P2'] and atual == prox:
                        k = j
                        while k < len(linha) and linha[k] == atual:
                            nova_linha[k] = atual
                            nova_tooltips[k] = f"Parte de uma sequência de {atual}"
                            k += 1
                        j = k
                    else:
                        j += 1
                for idx in range(len(nova_linha)):
                    if nova_linha[idx] == '' and linha[idx] in ['P1', 'P2']:
                        nova_linha[idx] = 'X'
                        nova_tooltips[idx] = 'Não faz parte de uma sequência'
                    elif nova_linha[idx] == '':
                        nova_linha[idx] = ''
                        nova_tooltips[idx] = ''

                df_seq.iloc[i] = nova_linha
                df_seq_tooltip.iloc[i] = nova_tooltips

            total_x_na_sequencia = (df_seq == 'X').sum().sum()


            with st.container(border=True):
                st.subheader(f"📈 Tabela de Resultados ({df_resultados.shape[0]}x{df_resultados.shape[1]})")
                st.markdown("Passe o mouse sobre as células **P1** ou **P2** para ver a explicação.")
                df_estilizado = df_resultados.style.set_tooltips(df_tooltips).apply(lambda col: col.map(estilizar_tabela))
                st.markdown(CSS_ESTILO_TABELA, unsafe_allow_html=True)
                st.write(df_estilizado.to_html(classes='styled-table', escape=False), unsafe_allow_html=True)
                
            st.subheader("📊 Resumo Geral dos Padrões")
            total_p1 = soma_p1_por_linha.sum()
            total_p2 = soma_p2_por_linha.sum()
            
            col_resumo1, col_resumo2 = st.columns([1, 1], gap="large")

            with col_resumo1:
                with st.container(border=True):
                    st.markdown("##### Contagem Total")
                    st.metric(label="🟣 Total de Padrões P1", value=total_p1)
                    st.metric(label="🧩 Total de Padrões P2", value=total_p2)
                    st.metric(label="❌ Total de 'X' na Tabela de Sequência", value=total_x_na_sequencia)
            with col_resumo2:
                with st.container(border=True):
                    st.markdown("##### Distribuição dos Padrões")
                    if total_p1 > 0 or total_p2 > 0:
                        df_resumo_grafico = pd.DataFrame({"P1": [total_p1], "P2": [total_p2]})
                        st.bar_chart(df_resumo_grafico, color=["#6f42c1", "#008F8C"])
                    else:
                        st.info("Nenhum padrão P1 ou P2 foi encontrado para exibir o gráfico.")
        
            # --- SEÇÃO DAS TABELAS DE LARGURA TOTAL ---
            if total_p1 > 0 or total_p2 > 0:
                st.divider()
                
                # --- Tabela de Sequências de P1/P2 ---
                with st.container(border=True):
                    st.subheader("🔍 Tabela de Sequências de P1/P2 (Apenas Consecutivas)")
                    df_seq_estilizado = df_seq.style.set_tooltips(df_seq_tooltip).apply(lambda col: col.map(estilizar_tabela))
                    st.markdown(CSS_ESTILO_TABELA, unsafe_allow_html=True)
                    html_da_tabela_seq = df_seq_estilizado.to_html(classes='styled-table', escape=False, index=True)
                    st.markdown(f'<div class="table-container">{html_da_tabela_seq}</div>', unsafe_allow_html=True)

               
        else:
            st.error("❌ A análise não produziu resultados.")
else:
    with st.container(border=True):
        st.info("✨ Seus resultados e o novo dashboard aparecerão aqui após a análise!")

st.sidebar.info("Analisador de Grid v9.0\n\n*Lógica Verificada & Tooltips Simplificados*")