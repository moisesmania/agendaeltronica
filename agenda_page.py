import streamlit as st
from database import create_db, adicionar_tarefa, excluir_tarefa, editar_tarefa, obter_tarefas

# Função para incluir o CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Certifique-se de criar o banco de dados e tabelas se não existirem
create_db()

def agenda_page():
    st.title("Lista de Tarefas")

    # Verifica se o usuário está logado
    if 'username' not in st.session_state:
        st.warning("Por favor, faça o login.")
        return

    username = st.session_state['username']

    # Entrada para adicionar tarefa
    descricao = st.text_input("Nova Tarefa:")

    # Botão para adicionar tarefa
    if st.button("Adicionar Tarefa"):
        if descricao:
            adicionar_tarefa(username, descricao)
            st.success("Tarefa adicionada!")
            #st.experimental_rerun()  # Atualiza a página para mostrar a nova tarefa
        else:
            st.warning("Por favor, adicione uma descrição para a tarefa.")

    # Listar tarefas associadas ao usuário logado
    tarefas = obter_tarefas(username)
    if tarefas:
        st.write("## Tarefas:")
        for tarefa in tarefas:
            concluida = "Concluída" if tarefa[3] else "Pendente"
            st.write(f"{tarefa[0]}: {tarefa[2]} - {concluida}")

        # Opções para editar e excluir tarefa
        opcao = st.selectbox("Editar ou Apagar:", ["Editar Tarefa", "Excluir Tarefa"])
        if opcao == "Editar Tarefa":
            id_tarefa = st.text_input("ID da Tarefa:")
            nova_descricao = st.text_input("Nova Descrição:")
            if st.button("Editar"):
                if id_tarefa and nova_descricao:
                    editar_tarefa(username, id_tarefa, nova_descricao)
                    st.success("Tarefa editada com sucesso!")
                    #st.experimental_rerun()  # Atualiza a página para mostrar as mudanças
                else:
                    st.warning("Por favor, insira o ID da tarefa e a nova descrição.")
        elif opcao == "Excluir Tarefa":
            id_tarefa = st.text_input("ID da Tarefa:")
            if st.button("Excluir"):
                if id_tarefa:
                    excluir_tarefa(username, id_tarefa)
                    st.success("Tarefa excluída com sucesso!")
                    #st.experimental_rerun()  # Atualiza a página para remover a tarefa excluída
                else:
                    st.warning("Por favor, insira o ID da tarefa para excluir.")
    else:
        st.write("Ainda não há tarefas adicionadas.")
        
        
    # Inclui o CSS
    load_css("styles.css")

        
    # Botão para sair da sessão
    if st.button("Sair"):
        st.session_state.clear()
        st.session_state.page = "login"

# Rodar a aplicação
agenda_page()
