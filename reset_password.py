import streamlit as st
import sqlite3

def reset_password(username, new_password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("UPDATE users SET password=? WHERE username=?", (new_password, username))
    conn.commit()
    conn.close()

def reset_password_page():
    st.title("Redefinir Senha")
    
    username = st.text_input("Nome de usuário")
    new_password = st.text_input("Nova senha", type="password")
    
    if st.button("Redefinir Senha"):
        if username and new_password:
            reset_password(username, new_password)
            st.success("Senha redefinida com sucesso!")
            st.session_state['page'] = 'login'
        else:
            st.error("Por favor, preencha todos os campos.")
