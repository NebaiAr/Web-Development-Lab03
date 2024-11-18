import streamlit as st
import google.generativeai as genai
import os
os.environ["GOOGLE_API_KEY"] = "AIzaSyCKpE5_kShn2_GcaL-oztw6Jn9_P9eITcs"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash") #this is the free model of google gemini
response = model.generate_content("Write a poem about how learning web development is fun!") #enter your prompt here!
print(response.text) #dont forget to print your response!

st.title("AI Battle Assistant")

 # response = req.get(f"{baseURL}/bosses?limit=1").json()
 # totalBosses = response.get("total")
    
 # # Calculate total number of pages based on limit (100 items per page)
 # limit = 100
 # totalPages = ((totalBosses + limit - 1) // limit) - 1

 # randomPage = random.randint(0, totalPages)
 # response = req.get(f"{baseURL}/bosses?limit={limit}&page={randomPage}").json()

 # # Randomly select a boss from the selected page
 # bosses = response.get("data") 
 # randomBoss = random.choice(bosses)
 # bossName = randomBoss["name"]
