import streamlit as st
from database import create_db, adicionar_tarefa, excluir_tarefas, editar_tarefa, obter_tarefas
from datetime import datetime

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
        st.write("Clique no botão abaixo para voltar à página de login.")
        if st.button("Voltar ao Login"):
            st.session_state['page'] = "login"
        return

    username = st.session_state['username']

    # Entrada para adicionar tarefa
    descricao = st.text_input("Nova Tarefa:")
    data = st.date_input("Data da Tarefa", datetime.today().date())
    
    # Entrada para hora como número (de 0 a 23)
    hora_num = st.number_input("Hora da Tarefa (0-23)", min_value=0, max_value=23, value=datetime.now().hour)
    minuto = st.number_input("Minuto da Tarefa (0-59)", min_value=0, max_value=59, value=datetime.now().minute)
    
    hora_str = f"{hora_num:02d}:{minuto:02d}:00"  # Formata a hora e minuto no formato HH:MM:SS

    # Botão para adicionar tarefa
    if st.button("Adicionar Tarefa"):
        if descricao:
            # Verificar se a tarefa já existe
            tarefas = obter_tarefas(username)
            tarefa_existe = any(
                tarefa[1] == descricao and tarefa[2] == data.strftime('%Y-%m-%d') and tarefa[3] == hora_str
                for tarefa in tarefas
            )
            
            if tarefa_existe:
                st.warning("A tarefa com a mesma descrição, data e hora já existe.")
            else:
                adicionar_tarefa(username, descricao, data.strftime('%Y-%m-%d'), hora_str)
                st.success("Tarefa adicionada!")
        else:
            st.warning("Por favor, adicione uma descrição para a tarefa.")

    # Listar tarefas associadas ao usuário logado
    tarefas = obter_tarefas(username)

    # Ordenar tarefas pela data e hora de adição em ordem decrescente
    tarefas_ordenadas = sorted(tarefas, key=lambda x: (x[5], x[6]), reverse=True)

    if tarefas_ordenadas:
        st.write("## Tarefas:")
        for tarefa in tarefas_ordenadas:
            if len(tarefa) >= 7:
                id_tarefa = tarefa[0]
                descricao_tarefa = tarefa[1]
                
                # Separar a data e hora de adição
                data_adicao_completa = tarefa[5]
                data_adicao, hora_adicao = data_adicao_completa.split(' ')  # Divide a string em data e hora
                
                # Converter e formatar a data no formato brasileiro
                data_adicao = datetime.strptime(data_adicao, '%Y-%m-%d').strftime('%d/%m/%Y')

                data_evento = datetime.strptime(tarefa[2], '%Y-%m-%d').strftime('%d/%m/%Y')
                hora_evento = tarefa[3]
                concluida = "Concluída" if tarefa[4] else "Pendente"

                st.write(f"""
                **ID =**                            {id_tarefa}
                **Descrição:**                     {descricao_tarefa}
                **Data e Hora da Adição:**      {data_adicao}  | {hora_adicao}
                **Data e Hora do Evento:**      {data_evento}  | {hora_evento}
                **Status:**                        {concluida}
                """)

            else:
                st.write(f"Tarefa com dados incompletos: {tarefa}")

        # Opções para editar e excluir tarefa
        opcao = st.selectbox("Editar ou Apagar:", ["Editar Tarefa", "Excluir Tarefa"])
        if opcao == "Editar Tarefa":
            id_tarefa = st.text_input("ID da Tarefa:")
            nova_descricao = st.text_input("Nova Descrição:")
            nova_data = st.date_input("Nova Data da Tarefa", datetime.today().date())
            nova_hora_num = st.number_input("Nova Hora da Tarefa (0-23)", min_value=0, max_value=23, value=datetime.now().hour)
            novo_minuto = st.number_input("Novo Minuto da Tarefa (0-59)", min_value=0, max_value=59, value=datetime.now().minute)
            nova_hora_str = f"{nova_hora_num:02d}:{novo_minuto:02d}:00"  # Formata a nova hora e minuto no formato HH:MM:SS
            
            if st.button("Editar"):
                if id_tarefa and nova_descricao:
                    editar_tarefa(username, id_tarefa, nova_descricao, nova_data.strftime('%Y-%m-%d'), nova_hora_str)
                    st.success("Tarefa editada com sucesso!")
                else:
                    st.warning("Por favor, insira o ID da tarefa e a nova descrição.")
        elif opcao == "Excluir Tarefa":
            id_inicial = st.number_input("ID Inicial da Tarefa:", min_value=1, value=1)
            id_final = st.number_input("ID Final da Tarefa:", min_value=1, value=1)
            if st.button("Excluir"):
                if id_inicial <= id_final:
                    excluir_tarefas(username, id_inicial, id_final)
                    st.success("Tarefas excluídas com sucesso!")
                else:
                    st.warning("O ID inicial deve ser menor ou igual ao ID final.")
    else:
        st.write("Ainda não há tarefas adicionadas.")
        
    # Inclui o CSS
    load_css("styles.css")

    # Botão para sair da sessão
    if st.button("Sair"):
        st.session_state.clear()
        st.session_state['page'] = "login"
