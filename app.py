import streamlit as st
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

# Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize ChatGroq client
llm = ChatGroq(
    temperature=0,
    groq_api_key=groq_api_key,
    model_name="llama-3.3-70b-versatile"
)

# Streamlit UI
st.set_page_config(page_title="AI Email Generator", layout="centered")

# Title
st.title("✉️ Templatized Email: AI-Powered Email Generator")

# Email Type Selection
email_type = st.radio("Select Email Type:", ["Compose New Email", "Reply To Email"], horizontal=True)

# Input Fields
col1, col2 = st.columns(2)
with col1:
    sender_name = st.text_input("Sender Name (Optional)", placeholder="Enter Sender Name")
with col2:
    receiver_name = st.text_input("Receiver Name (Optional)", placeholder="Enter Receiver Name")

purpose_of_email = st.text_area("Purpose of Email", placeholder="Enter the purpose of the email")

# Conditional Fields Based on Email Type
if email_type == "Compose New Email":
    email_subject = st.text_input("Email Subject (Optional)", placeholder="Enter Email Subject")
else:
    received_email = st.text_area("Received Email", placeholder="Paste the received email here")

# Tone and Length Dropdowns
col3, col4 = st.columns(2)
with col3:
    tone_of_voice = st.selectbox("Tone of Voice", ["None", "Formal", "Confident", "Academic", "Diplomatic", "Professional", "Friendly", "Casual"])
with col4:
    email_length = st.selectbox("Email Length", ["Short", "Medium", "Long"])

# Generate Button
if st.button("Generate"):
    with st.spinner("Generating your email..."):
        # Construct the prompt
        prompt_template = """
        Generate a {email_length} email with a {tone_of_voice} tone.
        Sender: {sender_name}
        Receiver: {receiver_name}
        Purpose: {purpose_of_email}
        """
        if email_type == "Compose New Email":
            prompt_template += "Subject: {email_subject}"
        else:
            prompt_template += "Reply to this email: {received_email}"

        prompt = PromptTemplate.from_template(prompt_template)

        # Prepare input variables
        input_vars = {
            "email_length": email_length.lower(),
            "tone_of_voice": tone_of_voice.lower(),
            "sender_name": sender_name,
            "receiver_name": receiver_name,
            "purpose_of_email": purpose_of_email,
            "email_subject": email_subject if email_type == "Compose New Email" else "",
            "received_email": received_email if email_type == "Reply To Email" else ""
        }

        # Generate the email
        try:
            chain = prompt | llm
            response = chain.invoke(input_vars)
            generated_email = response.content
            st.text_area("Generated Email", generated_email, height=200)
        except Exception as e:
            st.error(f"Error: {e}")