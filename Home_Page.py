import streamlit as st

# Title of App
st.title("Web Development Lab03")

# Assignment Data 
# TODO: Fill out your team number, section, and team members

st.header("CS 1301")
st.subheader("Team 53, Web Development - Section C")
st.subheader("Nathan Wilson, Nebai Araya")

st.image("Images/Elden_Ring2.jpg", caption="Flying Dragon Agheel from the game Elden Ring")
# Introduction
# TODO: Write a quick description for all of your pages in this lab below, in the form:
#       1. **Page Name**: Description
#       2. **Page Name**: Description
#       3. **Page Name**: Description
#       4. **Page Name**: Description

st.write("""
Welcome to our Streamlit Web Development Lab03 app! You can navigate between the pages using the sidebar to the left. The following pages are:

1. **Nebai Araya's Portfolio**: This page showcases Nebai Araya's portfolio, including his education, professional experience, projects, skills, and activities.
2. **Nathan Wilson's Portfolio**: This page showcases Nathan Wilson's portfolio, including his education, professional experience, projects, skills, and activities.
3. **Elden Ring Boss Finder**: This page is an Elden Ring boss search tool that has the user input a boss name (or have one randomly selected), which it uses to display information about the boss they searched. This includes dropped items, which the user can click on to view information about.
4. **IN DEVELOPMENT**: This page is currently in development and will be available soon.

""")

