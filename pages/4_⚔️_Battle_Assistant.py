import streamlit as st
import google.generativeai as genai
import os

model = genai.GenerativeModel("gemini-1.5-flash") #this is the free model of google gemini
response = model.generate_content("Write a poem about how learning web development is fun!") #enter your prompt here!


st.title("AI Battle Assistant")
st.write(response.text)
