from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
from dotenv import load_dotenv
import os
import streamlit as st
import asyncio

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")


external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

st.set_page_config("Quran", layout="wide")

st.title("📖 Quran Verse Finder")


user_input = st.text_input("Enter Surah name or Ayat range (Please limit to 40 ayat per request)")

if st.button("Get Quran"):
   if user_input:
      quran = Agent(
          name = "Translate Agent",
          instructions= """You are a Quran Arabic Agent. 
          When given the name of a Surah or a range of Ayat,
          If the Surah is long, respond in chunks (like 1-40, 41-80, 81-110). 
          If user only gives Surah name, send the first 40 Ayat and ask if they want more.
          you will respond with the exact Arabic of that Surah or those Ayat from the Quran,
          and give line by line ayat with clear ayat.
          Do not provide translation, explanation, or commentary.
          Only output the original Arabic Quranic as it is."""
)

      async def get_quran_response():
          response = await Runner.run(
              quran,
              input= user_input,
              run_config= config
      )
          return response.final_output
          
          
      with st.spinner("Fetching Quranic text..."):
          # Run async function inside Streamlit using asyncio
          quran_text = asyncio.run(get_quran_response())
  
      # st.text_area("Quranic Arabic", value=quran_text, height=300)
  
      st.markdown(
      """
      <div dir="rtl" style="text-align: right; font-size: 20px; line-height: 2; font-family: 'Scheherazade', 'Arial', sans-serif;">
          {}
      </div>
      """.format(quran_text.replace('\n', '<br>')),
      unsafe_allow_html=True
)
      
   else:
       st.warning("Please enter a Surah name or Ayat range first.")


    
    