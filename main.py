# Web Page Config
import streamlit as st

from db.conversations import get_all_conversations
from services.get_models_list import get_ollama_models_list
from services.get_title import  get_chat_title
from services.chat_utilities import get_answer
from db.conversations import (
    create_new_conversation,
    add_message,
    get_conversation,
    get_all_conversations
)
st.set_page_config(page_title="ChatGPT Clone", page_icon="⚽️", layout="centered")
st.title("🤖 Local ChatGPT Clone")

# Model to select drop down -select box
if "CONVOPRO_OLLAMA_MODELS" not in st.session_state:
    st.session_state.CONVOPRO_OLLAMA_MODELS = get_ollama_models_list()
selected_model=st.selectbox("Select Model", st.session_state.CONVOPRO_OLLAMA_MODELS)

# Session State default values
st.session_state.setdefault("conversation_id", None)
st.session_state.setdefault("conversation_title", None)
st.session_state.setdefault("chat_history", [])    # [{role, content}]

# Side bar : Conversations
with st.sidebar:
    st.header("🗨️ Chat History")
    conversations = get_all_conversations()  # {conv_id: title, conv_id: title}

    if st.button("➕ New Chat"):
        st.session_state.conversation_id = None
        st.session_state.conversation_title = None
        st.session_state.chat_history = []
    for cid, title in conversations.items():
        # Which conversation is currently open?
        is_current = cid ==st.session_state.conversation_id  # cid == st.session_state.conversaion_id # return True if user on that chat doc
        if is_current:
            label= f"**{title}**"  # Current chat appears bold in sidebar
        else:
            label= title
        # Making every chat as a clickable button
        if st.button(label= label, key= f"conv_{cid}"):
            doc=get_conversation(cid) or {}
            st.session_state.conversation_id=cid
            st.session_state.conversation_title=doc.get("title", "Untitled")
            st.session_state.chat_history=[
                {"role":msg["role"], "content":msg["content"]} for msg in doc.get("messages",[])
            ]
# Show chat so far
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_query=st.chat_input("Ask AI...")
if user_query:
    # 1. Show and Store User_query
    st.chat_message("user").markdown(user_query)
    st.session_state.chat_history.append({"role":"user", "content":user_query})

    # 2. Create conversation or append message to persist DB
    if st.session_state.conversation_id is None:
        try:
            title= get_chat_title(selected_model, user_query) or "New Chat"
        except Exception as e:
            st.error(f"Error in generating title:{e}")
            title="New Chat"
        conv_id=create_new_conversation(title=title,role="user", content=user_query)
        st.session_state.conversation_id=conv_id
        st.session_state.conversation_title=title
    else:
        add_message(conv_id=st.session_state.conversation_id, role="user", content=user_query)

    # 3. Assistant Chat Response
    try:
        assistant_text=get_answer(model_name=selected_model, chat_history=st.session_state.chat_history)
    except Exception as e:
        assistant_text=f"Error in getting response from model : {e}"

    # 4. Show and store assistant message
    with st.chat_message("assistant"):
        st.markdown(assistant_text)
    st.session_state.chat_history.append({"role":"assistant", "content":assistant_text})

    # 5. Persist assistant message
    if st.session_state.conversation_id:
        add_message(conv_id=st.session_state.conversation_id, role="assistant", content=assistant_text)
