import streamlit as st
import asyncio
import os
import extract_msg
from google import genai
import pandas as pd

"""
Combined Streamlit app that:
1) Allows single-file upload (.msg) classification.
2) Allows bulk folder-based classification of multiple .msg files.
"""

############################################
# Combined Email Classification App        #
############################################

# Ensure an event loop is available for google.genai
try:
    asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

# 1. Retrieve your Generative AI API key (replace with a secure method in production).
#    You can store the API key as an environment variable or in a secrets manager.
my_api_key = "xx"

# Initialize the GenAI client
client = genai.Client(api_key=my_api_key)

# Define a helper function to classify a single email
# Returns the model's classification text

def classify_email(subject: str, body: str) -> str:
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
        f"Subject: {subject}\n"
        f"Body:\n{body}\n"
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt_text
    )
    return response.text

# Streamlit App
st.title("Combined Single/Bulk Email Classification using Google GenAI")

mode = st.radio("Select Classification Mode", ("Single File", "Bulk Folder"))

if mode == "Single File":
    # Single-file upload
    st.write("Upload a .msg file to classify.")
    uploaded_file = st.file_uploader("Upload your .msg file", type=["msg"])

    if uploaded_file is not None:
        # Save the uploaded file to a temporary location
        # (Streamlit treats uploaded_file as a file-like object)
        with open("temp.msg", "wb") as f:
            f.write(uploaded_file.read())

        # Extract the email content
        msg = extract_msg.Message("temp.msg")
        email_subject = msg.subject or "[No Subject]"
        email_body = msg.body or "[No Body Found]"

        st.subheader("Email Subject")
        st.write(email_subject)

        st.subheader("Email Body")
        st.write(email_body)

        if st.button("Classify Email"):
            classification_result = classify_email(email_subject, email_body)
            st.subheader("Classification Result")
            st.write(classification_result)

else:
    # Bulk folder mode
    st.write("Enter a folder path containing multiple .msg files.")
    folder_path = st.text_input("Folder Path")

    if st.button("Classify All .msg in Folder"):
        if not folder_path:
            st.error("Please provide a valid folder path.")
        else:
            if not os.path.isdir(folder_path):
                st.error("Invalid folder path. Please try again.")
            else:
                msg_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".msg")]
                if not msg_files:
                    st.warning("No .msg files found in the specified folder.")
                else:
                    results = []
                    for msg_file in msg_files:
                        full_path = os.path.join(folder_path, msg_file)
                        try:
                            msg = extract_msg.Message(full_path)
                            subject = msg.subject or "[No Subject]"
                            body = msg.body or "[No Body Found]"

                            classification = classify_email(subject, body)

                            results.append({
                                "filename": msg_file,
                                "subject": subject,
                                "classification": classification
                            })
                        except Exception as e:
                            results.append({
                                "filename": msg_file,
                                "subject": "[Error Extracting Subject]",
                                "classification": f"Error: {e}"
                            })

                    if results:
                        df = pd.DataFrame(results)
                        csv_path = os.path.join(folder_path, "classification_results.csv")
                        df.to_csv(csv_path, index=False, encoding="utf-8-sig")

                        st.success(f"Classification complete. CSV saved to: {csv_path}")

                        # Optionally display a preview
                        st.write("Preview:")
                        st.dataframe(df)
