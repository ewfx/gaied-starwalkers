import streamlit as st
import os
import extract_msg
from google import genai

############################################
# Streamlit UI for Email Classification    #
############################################

# 1. Retrieve your Generative AI API key (replace with a secure method in production).
#    You can store the API key as an environment variable or in a secrets manager.
my_api_key = "AIzaSyDNc18Txt8Mv6Et6DiFi9ecoBwhUfJELkQ"

# Initialize the GenAI client
client = genai.Client(api_key=my_api_key)

st.title("Email Classification using Google GenAI")
st.write("Upload an .msg file and classify the email's content.")

# File uploader for .msg file
uploaded_file = st.file_uploader("Upload your .msg file", type=["msg"])

if uploaded_file is not None:
    # Save the uploaded file to a temporary location
    # (Streamlit treats uploaded_file as a file-like object)
    with open("temp.msg", "wb") as f:
        f.write(uploaded_file.read())

    # Extract the email content from the .msg file
    msg = extract_msg.Message("temp.msg")
    email_subject = msg.subject or "[No Subject]"
    email_body = msg.body or "[No Body Found]"

    st.subheader("Email Subject")
    st.write(email_subject)

    st.subheader("Email Body")
    st.write(email_body)

    # Define the classification prompt
    prompt_text = (
        f"You are an email classification assistant. I will provide you with the text of an email,\n"
        f"and you must determine which Request Type (and Sub Request Type, if applicable) from the following list "
        f"best describes the content of the email. These are all banking related terms:\n\n"
        f"1. Error Adjustment\n"
        f"- [No Sub Request Types]\n\n"
        f"2. Authorized Transfer\n"
        f"- [No Sub Request Types]\n\n"
        f"3. Deal/ Loan Closing Notice\n"
        f"   - Reallocation Fees\n"
        f"   - Amendment Fees\n"
        f"   - Reallocation Principal\n\n"
        f"4. Commitment Change\n"
        f"   - Cashless Roll\n"
        f"   - Decrease\n"
        f"   - Increase\n\n"
        f"5. Fee Payment\n"
        f"   - Ongoing Fee\n"
        f"   - Letter of Credit Fee\n\n"
        f"6. Money Movement - Inbound\n"
        f"   - Principal\n"
        f"   - Interest\n"
        f"   - Principal + Interest\n"
        f"   - Principal + Interest + Fee\n\n"
        f"7. Money Movement - Outbound\n"
        f"   - Foreign Currency\n"
        f"   - Timebound\n\n"
        f"INSTRUCTIONS:\n"
        f"- Read the email text carefully.\n"
        f"- Decide which Request Type it corresponds to.\n"
        f"- If the email indicates a specific Sub Request Type (e.g., “Reallocation Fees” or “Interest”), select that as well.\n"
        f"- If no Sub Request Type is indicated or relevant, only select the main Request Type.\n"
        f"- If the email does not correspond to any of the Request Types, select “Other”.\n\n"
        f"OUTPUT FORMAT:\n"
        f"- First, state the main Request Type.\n"
        f"- If applicable, also specify the relevant Sub Request Type.\n\n"
        f"Classify the type of email:\n\n"
        f"Subject: {email_subject}\n"
        f"Body:\n{email_body}\n"
    )

    if st.button("Classify Email"):
        # Send the prompt to the GenAI model
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt_text
        )
        classification_result = response.text

        st.subheader("Classification Result")
        st.write(classification_result)
