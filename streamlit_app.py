import streamlit as st
from streamlit_autorefresh import st_autorefresh
from datetime import datetime, timedelta
import time

st.set_page_config(page_title="Planner IA", layout="wide")

# dan: Inicialização das colunas do Kanban
def init_columns():
    return {
        "A Fazer": [],
        "Em Progresso": [],
        "Concluído": []
    }

if "kanban_data" not in st.session_state:
    st.session_state.kanban_data = init_columns()

if "pomodoro_running" not in st.session_state:
    st.session_state["pomodoro_running"] = False

if "pomodoro_start_time" not in st.session_state:
    st.session_state["pomodoro_start_time"] = None

# dan: Autorefresh ativado quando o timer estiver rodando
if st.session_state.get("pomodoro_running"):
    st_autorefresh(interval=1000, limit=None, key="pomodoro_refresh")

# dan: Pomodoro Timer com atualização automática
st.markdown("## ⏱️ Pomodoro Timer")
col1, col2 = st.columns([1, 4])

if col1.button("▶️ Iniciar 20 minutos"):
    st.session_state.pomodoro_start_time = time.time()
    st.session_state.pomodoro_running = True

if st.session_state.pomodoro_running:
    elapsed = int(time.time() - st.session_state.pomodoro_start_time)
    remaining = max(0, 20 * 60 - elapsed)
    minutes = remaining // 60
    seconds = remaining % 60
    col2.markdown(f"### ⌛ Tempo restante: {minutes:02d}:{seconds:02d}")
    if remaining == 0:
        st.success("⏰ Tempo encerrado! Faça uma pausa!")
        st.session_state["pomodoro_running"] = False

# dan: Renderização de cada card com botões de movimentação
def render_card(card, idx, column_key):
    with st.expander(f"{card['title']}"):
        st.text_area("Comentário", value=card['comment'], key=f"comment_{column_key}_{idx}")
        st.date_input("Data de Conclusão", value=card['due_date'], key=f"due_{column_key}_{idx}")
        cols = st.columns([1, 1])
        if column_key != "A Fazer":
            if cols[0].button("⬅️", key=f"left_{column_key}_{idx}"):
                move_card(column_key, idx, direction="left")
        if column_key != "Concluído":
            if cols[1].button("➡️", key=f"right_{column_key}_{idx}"):
                move_card(column_key, idx, direction="right")

# dan: Adicionar novo card
def add_card(column):
    with st.form(key=f"form_add_card_{column}"):
        title = st.text_input(f"Novo card para '{column}'", key=f"new_card_input_{column}")
        submitted = st.form_submit_button(f"Adicionar em {column}")
        if submitted and title:
            st.session_state.kanban_data[column].append({
                "title": title,
                "comment": "",
                "due_date": datetime.today()
            })

# dan: Mover card entre colunas
def move_card(current_col, idx, direction):
    cols = list(st.session_state.kanban_data.keys())
    current_idx = cols.index(current_col)
    new_idx = current_idx - 1 if direction == "left" else current_idx + 1
    if 0 <= new_idx < len(cols):
        card = st.session_state.kanban_data[current_col].pop(idx)
        st.session_state.kanban_data[cols[new_idx]].append(card)

# dan: Interface do Kanban
cols = st.columns(len(st.session_state.kanban_data))

for idx, (col_name, cards) in enumerate(st.session_state.kanban_data.items()):
    with cols[idx]:
        st.markdown(f"### {col_name}")
        add_card(col_name)
        for i, card in enumerate(cards):
            render_card(card, i, col_name)

# dan: Atualização do conteúdo dos cards após edição
for col_name, cards in st.session_state.kanban_data.items():
    for i, card in enumerate(cards):
        card['comment'] = st.session_state.get(f"comment_{col_name}_{i}", card['comment'])
        card['due_date'] = st.session_state.get(f"due_{col_name}_{i}", card['due_date'])

# dan: Atualização do conteúdo dos cards após edição
for col_name, cards in st.session_state.kanban_data.items():
    for i, card in enumerate(cards):
        card['comment'] = st.session_state.get(f"comment_{col_name}_{i}", card['comment'])
        card['due_date'] = st.session_state.get(f"due_{col_name}_{i}", card['due_date'])
