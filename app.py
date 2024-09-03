import streamlit as st
from login import login_page
from reset_password import reset_password_page
from register import register_page
from main_page import main_page
from agenda_page import agenda_page
import database  # Certifica que o banco de dados e a tabela são criados

# Configurar a página
st.set_page_config(
    page_title="Agenda Eletrônica",
    page_icon="pc_agenda.png"    
)

# Função para incluir o CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True) 

def main():
    if 'page' not in st.session_state:
        st.session_state['page'] = 'login'
    
    if 'logged_in' in st.session_state and st.session_state['logged_in']:
        if st.session_state['page'] == 'agenda':
            agenda_page()
        else:
            main_page()
    elif st.session_state['page'] == 'login':
        login_page()
    elif st.session_state['page'] == 'reset_password':
        reset_password_page()
    elif st.session_state ['page'] == 'register':
        register_page()
        
    # Inclui o CSS
    load_css("styles.css")        

if __name__ == "__main__":
    main()
