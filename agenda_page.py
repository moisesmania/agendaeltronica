import streamlit as st
import pandas as pd
from datetime import datetime
from database import add_event, get_events, delete_event, update_event

# Função para incluir o CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Função para normalizar as chaves dos eventos
def normalize_event_keys(events):
    """Normaliza as chaves dos eventos para que o frontend use 'Descrição', 'Data', e 'Hora'."""
    for event in events:
        if 'Description' in event:
            event['Descrição'] = event.pop('Description')  # Renomeia 'Description' para 'Descrição'
        if 'Date' in event:
            event['Data'] = event.pop('Date')  # Renomeia 'Date' para 'Data'
        if 'Time' in event:
            event['Hora'] = event.pop('Time')  # Renomeia 'Time' para 'Hora'
    return events

# Função para exibir a tabela de eventos
def display_events_table(events):
    # Converte a lista de eventos para um DataFrame
    events_df = pd.DataFrame(events)
    
    # Renomeia as colunas para o formato desejado
    events_df.rename(columns={"Date": "Data", "Time": "Hora", "Description": "Descrição"}, inplace=True)
    
    # Ajusta o formato das datas para o formato brasileiro
    events_df["Data"] = pd.to_datetime(events_df["Data"], format='%d/%m/%Y', errors='coerce').dt.strftime('%d/%m/%Y')
    
    # Reordena as colunas para que "Descrição" apareça primeiro
    events_df = events_df[["Descrição", "Data", "Hora"]]
    
    # Exibe a tabela
    st.dataframe(events_df, use_container_width=True, height=400)

    # Selecionar evento para edição ou exclusão
    selected_event_id = st.selectbox(
        "Escolha o evento para editar ou excluir:",
        options=[event['ID'] for event in events],
        format_func=lambda x: next(item['Descrição'] for item in events if item['ID'] == x),  # Usa 'Descrição'
        key="event_select"
    )
    
    if selected_event_id:
        selected_event = next(item for item in events if item['ID'] == selected_event_id)
        
        # Exibir opções de edição e exclusão
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Editar Evento", key=f"edit_{selected_event_id}"):
                st.session_state.event_id_to_edit = selected_event_id
                st.session_state.edit_date = datetime.strptime(selected_event['Data'], "%d/%m/%Y").date() if selected_event['Data'] else None
                st.session_state.edit_time = datetime.strptime(selected_event['Hora'], "%H:%M:%S").time() if selected_event['Hora'] else None
                st.session_state.edit_description = selected_event['Descrição']

        with col2:
            if st.button("Excluir Evento", key=f"delete_{selected_event_id}"):
                delete_event(st.session_state.username, selected_event_id)
                st.success("Evento excluído com sucesso!")
                st.session_state.events = get_events(st.session_state.username)

# Função de logout
def logout():
    st.session_state.clear()  # Limpa todos os dados da sessão
    st.write("Você foi desconectado com sucesso. Clique para ser redirecionado para a página de login...")
    st.stop()

# Página de agenda com tabela de eventos
def agenda_page():
    st.title("Agenda de Eventos")
    username = st.session_state.username

    # Inclui o CSS
    load_css("styles.css")

    # Container principal
    with st.container():
        st.header("Adicionar Evento")

        # Reorganizando o formulário com os campos na ordem desejada
        with st.form(key="add_event_form"):
            # Descrição do evento
            description = st.text_input("Descrição do Evento", placeholder="Ex: Reunião com o cliente")
            
            # Data do evento
            date = st.date_input("Data")
            
            # Hora do evento
            time = st.time_input("Hora")
            
            # Botão de adicionar evento
            if st.form_submit_button("Adicionar Evento"):
                formatted_date = date.strftime('%d/%m/%Y')
                formatted_time = time.strftime('%H:%M:%S')
                add_event(username, formatted_date, formatted_time, description)
                st.success("Evento adicionado com sucesso!")
                st.session_state.events = get_events(username)

    with st.container():
        st.header("Seus Agendamentos")
        if 'events' not in st.session_state:
            st.session_state.events = get_events(username)
        
        # Normaliza as chaves dos eventos para evitar erro de chave
        events = normalize_event_keys(st.session_state.events)
        
        if events:
            display_events_table(events)
            
            if 'event_id_to_edit' in st.session_state:
                st.write("### Editar Evento")
                
                edit_date = st.session_state.get('edit_date', datetime.now().date())
                edit_time = st.session_state.get('edit_time', datetime.now().time())
                edit_description = st.session_state.get('edit_description', '')
                
                new_date = st.date_input("Nova Data", value=edit_date)
                new_time = st.time_input("Nova Hora", value=edit_time)
                new_description = st.text_input("Nova Descrição", value=edit_description)

                if st.button("Salvar Alterações"):
                    formatted_new_date = new_date.strftime('%d/%m/%Y')
                    formatted_new_time = new_time.strftime('%H:%M:%S')
                    update_event(username, st.session_state.event_id_to_edit, formatted_new_date, formatted_new_time, new_description)
                    st.success("Evento atualizado com sucesso!")
                    del st.session_state.event_id_to_edit
                    st.session_state.events = get_events(username)
        else:
            st.info("Nenhum evento encontrado.")
        
        if st.button("Sair"):
            logout()
