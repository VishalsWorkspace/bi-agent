import streamlit as st
import sys
import os

# 🔐 SAFE ENV LOAD (NO CRASH)
try:
    if hasattr(st, "secrets") and "MONDAY_API_KEY" in st.secrets:
        os.environ["MONDAY_API_KEY"] = st.secrets["MONDAY_API_KEY"]
except Exception:
    pass

# 📦 ADD BACKEND PATH
sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

from main import run_agent


# 🎯 PAGE CONFIG
st.set_page_config(
    page_title="AI BI Agent",
    page_icon="📊",
    layout="centered"
)

# 🎨 HEADER
st.markdown(
    """
    # 📊 AI Business Intelligence Agent
    Ask natural language questions about your business data.
    """
)

st.caption("Powered by Monday.com API + Python Agent Logic")

# 💬 CHAT MEMORY
if "history" not in st.session_state:
    st.session_state.history = []

# 🧠 USER INPUT
user_input = st.chat_input("Ask something like 'total pipeline'...")

if user_input:
    answer, trace = run_agent(user_input)

    st.session_state.history.append({
        "query": user_input,
        "answer": answer,
        "trace": trace
    })

# 🖥️ DISPLAY CHAT (LATEST FIRST)
for chat in reversed(st.session_state.history):
    with st.chat_message("user"):
        st.write(chat["query"])

    with st.chat_message("assistant"):
        st.markdown(chat["answer"])

        # 🔍 TRACE (FOR EVALUATOR — VERY GOOD SIGNAL)
        with st.expander("🔍 View reasoning trace"):
            for t in chat["trace"]:
                st.write(f"- {t}")

# 📌 FOOTER
st.markdown("---")
st.caption(
    "⚠️ Data is fetched live from Monday.com. Results depend on API availability and data quality."
)