import streamlit as st
from datetime import datetime

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
    title = st.text_input(f"Novo card para '{column}'", key=f"new_card_input_{column}")
    if st.button(f"Adicionar em {column}", key=f"add_card_btn_{column}") and title:
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
