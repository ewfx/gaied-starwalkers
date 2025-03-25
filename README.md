# 🚀 Project Name

## 📌 Table of Contents
- [Introduction](#introduction)
- [Demo](#demo)
- [Inspiration](#inspiration)
- [What It Does](#what-it-does)
- [How We Built It](#how-we-built-it)
- [Challenges We Faced](#challenges-we-faced)
- [How to Run](#how-to-run)
- [Tech Stack](#tech-stack)
- [Team](#team)

---

## 🎯 Introduction
We developed a solution to streamline email classification within a banking or finance context. Our project focuses on automating the categorization of incoming messages based on specific types (e.g., Money Movement, Fee Payment, Commitment Change), ultimately tackling the complexity of manually handling large volumes of operational emails. By using powerful language models, we aim to reduce human error, save time, and create a more efficient workflow for financial teams.

## 🎥 Demo 
📹 [Video Demo] Check the repo for the demo videos.
🖼️ Screenshots: ![Screenshot 1](link-to-image)

## 💡 Inspiration
Our motivation stemmed from observing how front-office and operations teams grapple with ever-increasing email traffic—ranging from routine fee notifications to intricate loan amendments. Recognizing that these requests often require consistent, rule-based decisions, we saw a need for a robust, data-driven approach that could identify context, categorize emails, and serve recommended actions. We took inspiration from enterprise-scale problems like loan syndication and capital markets where even a single classification mistake can have costly repercussions.

## ⚙️ What It Does
Automated Classification: The system reads and interprets .msg files, extracting both subject and body to determine the appropriate request type.

Bulk Processing: It supports both single-email uploads and batch operations for entire directories, significantly cutting down on manual sorting overhead.

Generative AI Integration: Leveraging state-of-the-art AI models (via Google GenAI), our tool refines its categorization by analyzing linguistic cues and domain-specific keywords.

Exportable and Searchable Insights: Results are stored in structured formats (CSV), facilitating further analytics and reporting.

## 🛠️ How We Built It
Python & Streamlit: We chose Streamlit for rapid UI development and a clean user experience. Python’s simplicity allows us to integrate multiple libraries without sacrificing readability.

Extract_msg: This library handled Outlook .msg parsing, ensuring our solution can read metadata (subject, body, attachments) in detail.

Google GenAI: We used the google.genai client for classification tasks, providing robust language understanding. Its advanced NLP capabilities help us dissect complex email texts.

AsyncIO & Concurrency: To address potential threading or event-loop conflicts, we incorporated asyncio logic, ensuring stable concurrent calls to the AI APIs.

## 🚧 Challenges We Faced
Event Loop Conflicts: Integrating Google GenAI with Streamlit’s synchronous environment required careful handling of asyncio. We overcame runtime errors by initializing custom loops where necessary.

Data Extraction Nuances: Extracting meaningful text from .msg files (especially those with HTML bodies, special characters, or attachments) proved more complex than expected, mandating thorough testing.

Scalability: Handling batch classification across thousands of messages in one go required us to optimize I/O operations and ensure the AI calls remained efficient.

Domain Terminology: Banking and loan-related emails often contain intricate jargon—our system had to be carefully fine-tuned to recognize subtle differences (e.g., distinguishing “Reallocation Fees” from “Amendment Fees”).

By addressing these obstacles and applying a deep understanding of both technical and domain-specific details, our solution streamlines email classification for finance teams, bringing them closer to fully automated operational processes.

## 🏃 How to Run
1. Clone the repository  
   ```sh
   git clone https://github.com/your-repo.git
   ```
2. Install dependencies  
   ```sh
   pip install streamlit extract_msg google-genai asyncio os
   ```
3. Run the project  
   ```sh
   streamlit run main.py
   ```
4. Open your browser to the URL  http://localhost:8501).

## 🏗️ Tech Stack
- 🔹 Frontend: Streamlit
- 🔹 Backend: Python
- 🔹 LLM : Gemini 2

## 👥 Team
- **Saumya Sharma** - [GitHub](quitsune) | [LinkedIn](https://www.linkedin.com/in/saumya-sharma-4b9511194/)
- **Immaculate Maria Fernando** - [GitHub](#) | [LinkedIn](#)
