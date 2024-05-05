import os
import requests
import streamlit as st

st.set_page_config(page_title="Hospital System Chatbot", layout="wide")

with st.sidebar:
    st.header("About")
    st.markdown(
        """
        This chatbot integrates with a LangChain agent, specifically designed to address queries related 
        to a fictional hospital system. It provides information about hospitals, patients, visits, physicians, 
        and insurance payers using retrieval-augmented generation (RAG) techniques across both 
        structured and unstructured synthetically generated data.
        """
    )

    if st.button("View Repository"):
        import webbrowser
        webbrowser.open("https://github.com/GregoryTomy/hospital-llmops")

    st.header("Example Questions for a Healthcare Information System")

    st.subheader("Objective Queries")
    st.markdown("These queries involve precise data retrieval, often quantifiable and specific:")
    st.markdown("- Which hospitals are in the hospital system?")
    st.markdown("- What is the average duration in days for closed emergency visits?")
    st.markdown("- What was the total billing amount charged to each payer for 2023?")
    st.markdown("- What is the average billing amount for Medicaid visits?")
    st.markdown("- Which physician has the lowest average visit duration in days?")
    st.markdown("- How much was billed for patient 789's stay?")
    st.markdown("- What is the average billing amount per day for Aetna patients?")
    st.markdown("- Which state had the largest percent increase in Medicaid visits from 2022 to 2023?")

    st.subheader("Subjective Analysis")
    st.markdown("These questions require analysis of qualitative data such as patient feedback:")
    st.markdown("- At which hospitals are patients complaining about billing and insurance issues?")
    st.markdown("- What are patients saying about the nursing staff at Castaneda-Hardy?")
    st.markdown("- How many reviews have been written from patients in Florida?")
    st.markdown("- Which physician has received the most reviews for the visits they've attended?")

    st.subheader("Tool-Based Queries Using Tools")
    st.markdown("These questions require the agent to use specific tools for accurate information:")
    st.markdown("-What is the wait time at Wallace-Hamilton?")
    st.markdown("-Which hospital has the shortest wait time?")

st.title('Hospital System Chatbot')
st.subheader("By Gregory Tomy")
st.info("Feel free to ask me questions related to patients, visits, insurance payers, hospitals, physicians, reviews, and wait times!")

# Initialize session state for storing chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display each message stored in the session state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "output" in message.keys():
            st.markdown(message["output"])
        if "explanation" in message.keys():
            with st.status("How was this generated?", state="complete"):
                st.info(message["explanation"])

# Input field for user to ask questions
if prompt := st.chat_input("What would you like to know?"):
    st.chat_message("user").markdown(prompt)

    # Adds the user's question to the session state for preserving chat history
    st.session_state.messages.append(
        {"role": "user", "output": prompt}
    )

    # Prepare data for POST request to backend
    data = {"text": prompt}

    with st.spinner("Searching database..."):
        url = "http://chatbot-backend:8000/hospital-rag-agent"
        # url = "http://host.docker.internal:8000/hospital-rag-agent"
        # url = "http://0.0.0.0:8000/hospital-rag-agent"
        response = requests.post(url, json=data)

        if response.status_code == 200:
            output_text = response.json()["output"]
            explanation = response.json()["intermediate_steps"]
        else:
            output_text = "An error occured while processing your question. Please try agin or rephrase your message"
            explanation = output_text
    
    # Display the response from the backend in the chat interface
    st.chat_message("assistant").markdown(output_text)
    st.status("How was this generated?", state="complete").info(explanation)

    # Add the response to session state to preserve chat history
    st.session_state.messages.append(
        {
            "role": "assistant",
            "output": output_text,
            "explanation": explanation
        }
    )


