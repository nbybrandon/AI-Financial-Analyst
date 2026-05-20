import os
import datetime
import streamlit as st
from google import genai
from google.genai import types 
from dotenv import load_dotenv

# 1. Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# 2. Configure the web page
st.set_page_config(page_title="Wall Street AI", page_icon="📈")
st.title("📈 Wall Street Stock Analyst AI")
st.write("Real-time US market analysis powered by Gemini & Google Search.")

if not api_key:
    st.error("API Key not found. Please check your .env file.")
    st.stop()

# 3. Initialize the Google GenAI Client
client = genai.Client(api_key=api_key)

# 4. Create the System Instruction
today = datetime.date.today().strftime("%B %d, %Y")
system_prompt = f"""
You are an expert US stock market financial analyst. The current date is {today}.
Your job is to analyze stock performance, explain market trends, and summarize financial news.
Rules:
1. Always use the Google Search tool to fetch the most up-to-date stock prices and news before answering.
2. Be concise, professional, and use standard financial terminology.
3. ALWAYS include a brief disclaimer at the end of your response stating: 'Note: I am an AI, and this is not professional financial advice.'
"""

# 5. Create a "Memory" for the chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# 6. Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. The Chat Input Box
if prompt := st.chat_input("Ask about today's news..."):
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        try:
            # 8. Call the API with Search Grounding enabled!
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    # THIS IS THE MAGIC LINE: Give the AI the Google Search Tool
                    tools=[types.Tool(google_search=types.GoogleSearch())],
                )
            )
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error(f"An error occurred: {e}")