import streamlit as st

def main_page():
    st.title("Página de Boas Vindas")
    
    # Introdução ao sistema de agendamento
    st.subheader("Bem-vindo ao Sistema de Agendamento Moderno!")
    st.write("""
    Este sistema foi desenvolvido para ajudá-lo a gerenciar seus eventos e compromissos de maneira eficiente e segura.
    Com ele, você pode adicionar novos eventos, editar detalhes de eventos já cadastrados, e excluir aqueles que já não são mais necessários.
    
    Com a correria do dia a dia, manter tudo organizado pode ser um desafio. Nosso sistema simplifica esse processo, permitindo que você tenha controle total sobre sua agenda, garantindo que você nunca perca um compromisso importante.
    
    **Entre e confira as vantagens deste sistema**! Organize sua vida com facilidade, produtividade, e segurança.
    """)

    # Boas-vindas ao usuário
    st.write(f"Bem-vindo, {st.session_state['username']}!")

    # Botões para navegação
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Abrir Agenda"):
            st.session_state['page'] = 'agenda'
    
    with col2:
        if st.button("Sair"):
            st.session_state['logged_in'] = False
            st.session_state['username'] = None
            st.session_state['page'] = 'login'

# Exemplo de chamada da função main_page
if __name__ == "__main__":
    if 'username' not in st.session_state:
        st.session_state['username'] = 'Usuário'
    main_page()

