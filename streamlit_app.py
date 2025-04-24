import streamlit as st
from streamlit_sortable import sortable
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

# dan: Renderização de cada card

def render_card(card, idx, column_key):
    with st.expander(f"{card['title']}"):
        st.text_area("Comentário", value=card['comment'], key=f"comment_{column_key}_{idx}")
        st.date_input("Data de Conclusão", value=card['due_date'], key=f"due_{column_key}_{idx}")

# dan: Adicionar novo card

def add_card(column):
    title = st.text_input(f"Novo card para '{column}'", key=f"new_card_input_{column}")
    if st.button(f"Adicionar em {column}", key=f"add_card_btn_{column}") and title:
        st.session_state.kanban_data[column].append({
            "title": title,
            "comment": "",
            "due_date": datetime.today()
        })

# dan: Interface do Kanban
cols = st.columns(len(st.session_state.kanban_data))

for idx, (col_name, cards) in enumerate(st.session_state.kanban_data.items()):
    with cols[idx]:
        st.markdown(f"### {col_name}")
        add_card(col_name)

        moved = sortable(
            [card['title'] for card in cards],
            direction="vertical",
            key=f"sortable_{col_name}"
        )

        new_order = [next(c for c in cards if c['title'] == title) for title in moved]
        st.session_state.kanban_data[col_name] = new_order

        for i, card in enumerate(new_order):
            render_card(card, i, col_name)

# dan: Atualização do conteúdo dos cards após edição
for col_name, cards in st.session_state.kanban_data.items():
    for i, card in enumerate(cards):
        card['comment'] = st.session_state.get(f"comment_{col_name}_{i}", card['comment'])
        card['due_date'] = st.session_state.get(f"due_{col_name}_{i}", card['due_date'])
