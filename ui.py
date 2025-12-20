import streamlit as st
from agent import run_agent

st.set_page_config(
    page_title="Clinical Workflow Assistant",
    page_icon="🏥",
    layout="centered"
)

st.title("🏥 Clinical Workflow Assistant")
st.caption("Patient search • Insurance • Appointments")

# ---------------- Session ----------------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- Sidebar ----------------
st.sidebar.header("Quick Actions")

examples = [
    "Find patient Ravi Kumar",
    "Check insurance for PAT123",
    "Find appointment slots",
    "Book appointment for PAT123"
]

example = st.sidebar.selectbox("Examples", ["-- Select --"] + examples)

# ---------------- Input ----------------
user_input = st.text_input(
    "Clinician Input",
    value=example if example != "-- Select --" else ""
)

if st.button("Run Workflow"):
    if user_input.strip():
        with st.spinner("Processing..."):
            try:
                response = run_agent(user_input)
                st.session_state.history.append((user_input, response))
            except Exception as e:
                st.error(str(e))
    else:
        st.warning("Please enter a request")

# ---------------- Chat ----------------
st.divider()
st.subheader("Conversation")

for user, bot in reversed(st.session_state.history):
    with st.chat_message("user"):
        st.write(user)
    with st.chat_message("assistant"):
        st.write(bot)
