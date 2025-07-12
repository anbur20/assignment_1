# Import necessary packages
import streamlit as st
import mysql.connector
from datetime import datetime
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import time

db_host='gateway01.ap-southeast-1.prod.aws.tidbcloud.com'
db_user='2zfoFbFCnKGxKRW.root'
db_password='QdIF3FJ19vZSHlNs'
db_name='Placement_Eligibility'

# Connect to Database
db=mysql.connector.connect(host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
                             user="2zfoFbFCnKGxKRW.root",
                             password='QdIF3FJ19vZSHlNs',
                             port=4000,
                             database='Placement_Eligibility',
                             ssl_ca="C:/vscode/certs/ca.pem",
                             ssl_verify_cert=True)
dbcursor=db.cursor()

st.set_page_config(page_title="Placement Eligibility Application", layout="wide", initial_sidebar_state="expanded")

# Sidebar - Page Selection
page = st.sidebar.radio(" Selection List ", ["Home Page","Eligibility Filter", "Placement Insights"])

if page == "Home Page":
    st.title("Placement Eligibility Application ")
    st.write("Students Placement Portal")
    
elif page == "Eligibility Filter":
    st.title(" Student Placement Eligibility Dashboard ")
    # Input criteria
    min_soft_skills = st.slider("Minimum Soft Skills Score", min_value=50, max_value=100, value=70)
    min_problems_solved = st.slider("Minimum Problems Solved", min_value=10, max_value=200, value=50)
    
    # Fetch eligible students
    query = f"""
    SELECT s.student_id, s.name, s.age, s.course_batch, p.problems_solved, 
           ROUND((ss.communication + ss.teamwork + ss.presentation + ss.leadership + ss.critical_thinking + ss.interpersonal_skills) / 6, 2) AS avg_soft_skills,
           CASE WHEN p.problems_solved  >= {min_problems_solved}
                AND ROUND((ss.communication + ss.teamwork + ss.presentation + ss.leadership + ss.critical_thinking + ss.interpersonal_skills) / 6, 2) >= {min_soft_skills} 
                THEN 'Eligible' ELSE 'Not Eligible' END AS eligibility_status,
           pl.placement_status
    FROM Students_Table s
    JOIN Programming_Table p ON s.student_id = p.student_id
    JOIN Soft_Skill_Table ss ON s.student_id = ss.student_id
    JOIN Placement_Table pl ON s.student_id = pl.student_id
    """   
    conn = db
    df = pd.read_sql(query, conn)
    conn.close()
    
    st.dataframe(df)
# Date and Time to display with dynamically update
    time_placeholder = st.empty()

    while True:
        timenow = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
        time_placeholder.write(f"Current Date & Time: {timenow}")
        time.sleep(1)
elif page == "Placement Insights":
    st.title(" PLACEMENT INSIGHTs ")

 # Declare the dropdown list and the query relavant to it   
    queries = {
        "Average Placement Package": "SELECT AVG(placement_package) AS avg_package FROM Placement_Table",
        "Average Interview Rounds Cleared": "SELECT AVG(interview_rounds_cleared) AS avg_rounds FROM Placement_Table",
        "Internships vs. Placement": "SELECT internships_completed, COUNT(*) AS student_count FROM Placement_Table GROUP BY internships_completed",
        "Most Common Graduation Year Among Students": "SELECT graduation_year, COUNT(*) AS count FROM Students_Table GROUP BY graduation_year ORDER BY count DESC LIMIT 1",
        "Programming Language Popularity": "SELECT language, COUNT(*) AS student_count FROM Programming_Table GROUP BY language ORDER BY student_count DESC",
        "Placement Readiness Ratio": "SELECT placement_status, COUNT(*) AS student_count FROM Placement_Table GROUP BY placement_status",
        "Soft Skills Performance Distribution": "SELECT AVG(communication) AS avg_comm, AVG(teamwork) AS avg_teamwork, AVG(presentation) AS avg_presentation FROM Soft_Skill_Table",
        "Top 5 Students by Problems Solved": "SELECT s.name, p.problems_solved FROM Students_Table s JOIN Programming_Table p ON s.student_id = p.student_id ORDER BY p.problems_solved DESC LIMIT 5",
        "Top 5 Students by Mock Interview Score": "SELECT s.name, p.mock_interview_score FROM Students_Table s JOIN Placement_Table p ON s.student_id = p.student_id ORDER BY p.mock_interview_score DESC LIMIT 5",
        "Top Companies Hiring": "SELECT company_name, COUNT(*) AS student_count FROM Placement_Table GROUP BY company_name ORDER BY student_count DESC LIMIT 5"
    }
    
    # Dropdown to select a query
    selected_query = st.selectbox("Select an Insight", list(queries.keys()))
    
    # Fetch and display the result for the selected query
    conn = db
    query = queries[selected_query]
    df = pd.read_sql(query, conn)
    conn.close()
    
    # Display the result
    st.subheader(selected_query)
    st.dataframe(df)

# Date and Time to display with dynamically update
    time_placeholder = st.empty()

    while True:
        timenow = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
        time_placeholder.write(f"Current Date & Time: {timenow}")
        time.sleep(1)