import streamlit as st
from main import run_agent

with st.sidebar:
    st.markdown("## ℹ️ About this app")

    with st.expander("Learn more"):
        st.markdown("""
        This application is a simple AI-powered knowledge assistant built using OpenAI APIs.

        It demonstrates a basic implementation of Retrieval-Augmented Generation (RAG), where responses are generated based on a custom knowledge base rather than relying solely on the model’s internal knowledge.

        The system includes:
        - A lightweight document retrieval mechanism using keyword matching
        - Tool-based reasoning (search + calculator)
        - A Streamlit interface for interactive querying

        ⚠️ Note: The knowledge base is limited and may not cover all topics. Responses are constrained to the available data and may not always be comprehensive.
        """)

st.set_page_config(page_title="AI Knowledge Assistant", page_icon="🧠")

st.title("🧠 AI Knowledge Assistant")
st.markdown("Ask questions based on your custom knowledge base")

user_question = st.text_input("💬 Enter your question:")

st.markdown("### 💡 Try these:")
st.write("- What are AI agents?")
st.write("- How many species of cats are there?")
st.write("- 25 * 6 + 10")

if st.button("Ask"):
    if user_question.strip() == "":
        st.warning("Please enter a question")
    else:
        with st.spinner("Thinking..."):
            answer = run_agent(user_question)

        st.write(answer)