import streamlit as st

from utils import render_messages, create_chatbot


# ------------------------------网页------------------------------
page_title = "Chatbot"  # 网页标题
st.set_page_config(
    page_title=page_title,
    page_icon="💬",
    menu_items={
        "About": "Hi! **Jamie** developed me! Contact him [here](https://github.com/dwjamie/ChatLLM) if you have any problems."
    },
)

# ------------------------------配置------------------------------
# 侧边栏配置
with st.sidebar:
    st.header("Chatbot Settings")
    system_message = st.text_area(
        label="Character", placeholder="What character does the robot need to play?"
    )
    model = st.selectbox(
        "Model",
        options=[
            "GPT-4 Turbo",
            "GPT-3.5 Turbo",
            "Claude 3 Opus",
            "Claude 3 Sonnet",
            "Claude 3 Haiku",
            "Claude 2.1",
        ],
        index=2,
    )
    temperature = st.slider(
        "Randomness", min_value=0.0, max_value=1.0, step=0.01, value=0.0
    )
    change_config = st.button(label="Confirm Settings")
    clean_history = st.button(label="Clear Conversation History")

# 若第一次进入网页或切换了页面，则重置对话历史
if "current_page" not in st.session_state:
    st.session_state.current_page = page_title
if st.session_state.current_page != page_title or "chatbot" not in st.session_state:
    st.session_state.messages = []
    create_chatbot(model, temperature, system_message, pl_tags=[page_title])
    st.session_state.current_page = page_title

# 清空对话历史并重置ChatBot
if clean_history:
    st.session_state.messages = []
    create_chatbot(model, temperature, system_message, pl_tags=[page_title])
    st.info("Conversation history has been cleared!", icon="✅")

# 确认ChatBot配置
if change_config:
    create_chatbot(model, temperature, system_message, pl_tags=[page_title])
    st.info("Chatbot settings confirmed!", icon="✅")

# ------------------------------对话------------------------------
st.title(page_title)  # 渲染标题
render_messages(st.session_state.messages)  # 渲染对话历史
if user_message := st.chat_input("Hello!"):
    # 渲染并储存用户消息
    with st.chat_message(name="user", avatar="🧑‍💻"):
        st.markdown(user_message)
    st.session_state.messages.append({"role": "user", "content": user_message})

    # 发给ChatBot
    assistant_response = st.session_state.chatbot.chat(user_message)

    # 渲染并储存ChatBot消息
    assistant_message = ""
    with st.chat_message(name="assistant", avatar="🤖"):
        placeholder = st.empty()
        for token in assistant_response:
            assistant_message += token
            placeholder.write(assistant_message + "▌")
        placeholder.empty()
        st.markdown(assistant_message)

    st.session_state.chatbot.add_message("assistant", assistant_message)
    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_message}
    )
