'''Lab 3 portfolio :D'''

import streamlit as st
import info_Nathan
import pandas as pd

#About me!

def aboutMe():
    st.header("About Me!")
    st.image(info_Nathan.profile_picture, width=200)
    st.write(info_Nathan.about_me)
    st.write('---')
aboutMe()

#Links (AKA Sidebar)

def sideBar():
    st.sidebar.header("Other Links")
    st.sidebar.text("View my LinkedIn profile,")
    linkedInLink = f'<a href="{info_Nathan.my_linkedin_url}"><img src="{info_Nathan.linkedin_image_url}" alt="LinkedIn" width="75" height="75"></a>'
    st.sidebar.markdown(linkedInLink, unsafe_allow_html=True)
    st.sidebar.text("check out my work on GitHub,")
    gitHubLink = f'<a href="{info_Nathan.my_github_url}"><img src="{info_Nathan.github_image_url}" alt="Github" width="75" height="75"></a>'
    st.sidebar.markdown(gitHubLink, unsafe_allow_html=True)
    st.sidebar.text("or, email me!")
    emailHTML = f'<a href="{info_Nathan.my_email_address}"><img src="{info_Nathan.email_image_url}" alt="Email" width="75" height="75"></a>'
    st.sidebar.markdown(emailHTML, unsafe_allow_html=True)
sideBar()

#Education History

def education(education_data, course_data):
    st.header("Education")
    st.subheader(f"**{education_data['Institution']}**")
    st.write(f"**Degree:** {education_data['Degree']}")
    st.write(f"**Graduation Date:** {education_data['Graduation Date']}")
    st.write(f"**GPA:** {education_data['GPA']}")
    st.write("**Relevant Coursework**")
    courseWork = pd.DataFrame(course_data)
    st.dataframe(courseWork, column_config={
        "code": "Course Code",
        "names": "Course Names",
        "semester_taken": "Semester Taken",
        "skills": "What I Learned"},
        hide_index=True
        )
    st.write('---')
education(info_Nathan.education_data, info_Nathan.course_data)

#Professional Experience

def experience(experienceData):
    st.header("Professional Experience")
    for jobTitle, (jobDescription, ) in experienceData.items():
        expander = st.expander(f"{jobTitle}")
        #expander.image(image, width=250)
        for bullet in jobDescription:
            expander.write(bullet)
    st.write('---')
experience(info_Nathan.experience_data)

#Projects

def projects(projectsData):
    st.header("Projects")
    for projectName, projectDesc in projectsData.items():
        expander = st.expander(f"{projectName}")
        expander.write(projectDesc)
    st.write("---")
projects(info_Nathan.projects_data)

#Skills

def skills(programmingData, spokenData):
    st.header("Skills")
    st.subheader("Programming Languages")
    for skill, percent in programmingData.items():
        st.write(f"{skill}{info_Nathan.programming_icons.get(skill)}")
        st.progress(percent)
    st.subheader("Spoken Languages")
    for spoken, proficiency in spokenData.items():
        st.write(f"{spoken} {info_Nathan.spoken_icons.get(spoken,)}: {proficiency}")
    st.write('---')
skills(info_Nathan.programming_data, info_Nathan.spoken_data)

#Activities

def activities(leadershipData, activityData):
    st.header("activities")
    leadership, activities = st.tabs(['Leadership', 'Other'])
    with leadership:
        st.subheader('Leadership')
        for title, (details) in leadershipData.items():
            expander = st.expander(f"{title}")
            for bullet in details:
                expander.write(bullet)
    with activities:
        st.subheader("Other Activities")
        for title, detail in activityData.items():
            expander = st.expander(f'{title}')
            for bullet in detail:
                expander.write(bullet)
    st.write('---')
activities(info_Nathan.leadership_data, info_Nathan.activity_data)
