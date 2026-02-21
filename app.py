import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Lean ROI Calculator - Beatriz Cruz", layout="wide")

st.title("Lean ROI Calculator")
st.markdown("""
Esta ferramenta quantifica o impacto financeiro de automações e melhorias de processos. 
Ideal para validação de projetos **Lean Seis Sigma**.
""")

# Barra lateral para parâmetros globais
st.sidebar.header("Parâmetros de Custo")
custo_hh = st.sidebar.number_input("Custo da Hora Técnica (R$)", value=20.0, step=5.0)

# Entrada de dados das tarefas
st.subheader("📋 Detalhamento de Tarefas")
if 'tarefas' not in st.session_state:
    st.session_state.tarefas = [
        {"Tarefa": "Automação de Emails Diários", "H_Antes": 0.5, "H_Depois": 0.083, "Freq": 22},
        {"Tarefa": "Automações de Bases | Lavador", "H_Antes": 0.15, "H_Depois": 0.01, "Freq": 22},
        {"Tarefa": "Automações de Bases | Triângulo", "H_Antes": 0.28, "H_Depois": 0.01, "Freq": 22},
        {"Tarefa": "OnePage", "H_Antes": 1, "H_Depois": 0.083, "Freq": 22}
    ]

# Formulário para adicionar novas tarefas
with st.expander("Adicionar Nova Tarefa"):
    with st.form("form_tarefa"):
        nome = st.text_input("Nome da Atividade")
        h_ant = st.number_input("Horas antes (Manual)", min_value=0.1)
        h_dep = st.number_input("Horas depois (Automatizado)", min_value=0.0)
        freq = st.number_input("Frequência Mensal", min_value=1)
        if st.form_submit_button("Adicionar"):
            st.session_state.tarefas.append({"Tarefa": nome, "H_Antes": h_ant, "H_Depois": h_dep, "Freq": freq})
            st.rerun()

# Processamento dos Dados
df = pd.DataFrame(st.session_state.tarefas)
df['Horas Economizadas/Mês'] = (df['H_Antes'] - df['H_Depois']) * df['Freq']
df['Economia Mensal (R$)'] = df['Horas Economizadas/Mês'] * custo_hh
df['Economia Anual (R$)'] = df['Economia Mensal (R$)'] * 12

# Exibição dos Resultados
st.dataframe(df.style.format({"Economia Mensal (R$)": "R$ {:.2f}", "Economia Anual (R$)": "R$ {:.2f}"}))

# Métricas de Impacto
total_anual = df['Economia Anual (R$)'].sum()
st.metric("Economia Total Anual Estimada", f"R$ {total_anual:,.2f}")
