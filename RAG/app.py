import streamlit as st
import requests
import time

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Smart RAG Chatbot", layout="wide")

st.title("🤖 Smart Personalized RAG Chatbot")

# ------------------------
# Initialize Session State
# ------------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "uploaded_file_name" not in st.session_state:
    st.session_state.uploaded_file_name = None

if "summary_length" not in st.session_state:
    st.session_state.summary_length = "medium"

if "pref_sent" not in st.session_state:
    st.session_state.pref_sent = False

# ------------------------
# Sidebar Controls
# ------------------------
st.sidebar.header("📂 Document Control")

# Show active document
if st.session_state.uploaded_file_name:
    st.sidebar.success(
        f"Active Document:\n{st.session_state.uploaded_file_name}"
    )

# New Chat Button
if st.sidebar.button("🆕 New Chat"):
    st.session_state.history = []
    st.rerun()

# ------------------------
# User Preferences
# ------------------------
st.sidebar.header("⚙️ Preferences")

summary_length = st.sidebar.selectbox(
    "Summary Length",
    ["short", "medium", "long"],
    index=["short", "medium", "long"].index(
        st.session_state.summary_length
    )
)

# Send preference ONLY if changed
if summary_length != st.session_state.summary_length:

    st.session_state.summary_length = summary_length

    try:
        requests.post(
            f"{API_URL}/set_preferences",
            json={"summary_length": summary_length}
        )
    except:
        pass

# ------------------------
# File Upload
# ------------------------
uploaded_file = st.sidebar.file_uploader(
    "Upload PDF or TXT",
    type=["pdf", "txt"]
)

# ------------------------
# Upload Logic
# ------------------------
if uploaded_file and uploaded_file.name != st.session_state.uploaded_file_name:

    progress_container = st.sidebar.container()

    with progress_container:

        st.write("🚀 Processing document...")
        progress_bar = st.progress(0)
        percent_text = st.empty()
        status_text = st.empty()

        # Upload animation
        for i in range(0, 40):
            progress_bar.progress(i)
            percent_text.markdown(f"**{i}%**")
            status_text.caption("Uploading document...")
            time.sleep(0.02)

        files = {
            "file": (uploaded_file.name, uploaded_file.getvalue())
        }

        try:
            res = requests.post(
                f"{API_URL}/upload",
                files=files
            )

            # Index animation
            for i in range(40, 90):
                progress_bar.progress(i)
                percent_text.markdown(f"**{i}%**")
                status_text.caption("Analyzing & indexing document...")
                time.sleep(0.03)

            if res.status_code == 200:

                progress_bar.progress(100)
                percent_text.markdown("**100%**")
                status_text.success("✅ Document uploaded & indexed!")

                st.session_state.uploaded_file_name = uploaded_file.name
                st.session_state.history = []

                time.sleep(0.5)
                st.rerun()

            else:
                status_text.error("❌ Upload failed")

        except Exception:
            status_text.error("⚠️ Backend not reachable")

# ------------------------
# Chat Section
# ------------------------
st.subheader("💬 Ask Questions From Your Documents")

query = st.chat_input("Ask a question...")

if query:

    st.session_state.history.append(("user", query))

    with st.spinner("🤖 Thinking..."):

        try:
            res = requests.get(
                f"{API_URL}/chat",
                params={"query": query}
            ).json()

            answer = res.get("response", "No response")
            intent = res.get("intent", "unknown")

            # ⭐ NEW TRUST METRICS (ADDED)
            risk = res.get("hallucination_risk", "unknown")
            score = res.get("quality_score", 0)
            unsupported = res.get("unsupported_sentences", [])

            if risk == "LOW":
                badge = "🟢 Reliable"
            elif risk == "MEDIUM":
                badge = "🟡 Verify"
            else:
                badge = "🔴 Low Confidence"

            st.session_state.history.append(
                (
                    "assistant",
                    f"""{answer}

🧠 Intent: {intent}
🛡 Risk: {risk}
⭐ Quality: {score}
{badge}
"""
                )
            )

        except Exception:
            st.session_state.history.append(
                ("assistant", "⚠️ Error connecting to backend")
            )

# ------------------------
# Display Chat History
# ------------------------
for role, message in st.session_state.history:

    if role == "user":
        with st.chat_message("user"):
            st.write(message)

    else:
        with st.chat_message("assistant"):
            st.write(message)

            # ⭐ OPTIONAL CONFIDENCE BAR (ADDED)
            try:
                if "⭐ Quality:" in message:
                    score_value = float(message.split("⭐ Quality:")[1].split()[0])
                    st.progress(score_value / 100)
            except:
                pass
