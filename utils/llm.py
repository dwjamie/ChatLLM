import streamlit as st
import agent


def create_chatbot(model, temperature, system_message, functions=None, pl_tags=[]):
    if model == "GPT-3.5":
        st.session_state.chatbot = agent.OpenAI(
            functions=functions,
            model="gpt-3.5-turbo-1106",
            temperature=temperature,
            pl_tags=pl_tags,
        )
    elif model == "GPT-4":
        st.session_state.chatbot = agent.OpenAI(
            functions=functions, model="gpt-4-1106-preview", temperature=temperature, pl_tags=pl_tags
        )
    elif model == "Claude 1":
        st.session_state.chatbot = agent.Claude(
            model="claude-1", temperature=temperature, pl_tags=pl_tags
        )
    elif model == "Claude 2":
        st.session_state.chatbot = agent.Claude(
            model="claude-2", temperature=temperature, pl_tags=pl_tags
        )
    elif model == "Claude Instant":
        st.session_state.chatbot = agent.Claude(
            model="claude-instant-1", temperature=temperature, pl_tags=pl_tags
        )
    if system_message:
        st.session_state.chatbot.add_message(
            "system",
            system_message,
        )
    for message in st.session_state.messages:
        st.session_state.chatbot.add_message(message["role"], message["content"])
