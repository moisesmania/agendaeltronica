import streamlit as st
from login import login_page
from reset_password import reset_password_page
from register import register_page
from main_page import main_page
from agenda_page import agenda_page

# Configuração da página
st.set_page_config(page_title="Agenda Top!", page_icon="pc_agenda.png", layout="centered")

# Função para incluir o CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
    # Inclui o CSS
    load_css("styles.css")

    # Verifica se o usuário está logado e se a página está definida
    if 'page' not in st.session_state:
        st.session_state['page'] = 'login'
    
    if 'username' in st.session_state:
        if st.session_state['page'] == 'agenda':
            agenda_page()
        elif st.session_state['page'] == 'main':
            main_page()
        elif st.session_state['page'] == 'reset_password':
            reset_password_page()
        elif st.session_state['page'] == 'register':
            register_page()
    else:
        if st.session_state['page'] == 'login':
            login_page()
        else:
            st.warning("Por favor, faça o login.")
            st.write("Clique no botão abaixo para voltar à página de login.")
            if st.button("Voltar ao Login"):
                st.session_state['page'] = 'login'
    
if __name__ == "__main__":
    main()
