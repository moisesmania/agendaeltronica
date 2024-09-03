import streamlit as st

def main_page():
    st.title("Página Principal")
    st.write(f"Bem-vindo, {st.session_state['username']}!")

    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Abrir Agenda"):
            st.session_state['page'] = 'agenda'
    
    with col2:
        if st.button("Sair"):
            st.session_state['logged_in'] = False
            st.session_state['username'] = None
            st.session_state['page'] = 'login'
