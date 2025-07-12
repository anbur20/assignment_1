# assignment_1
Placement Eligibility App. 
#
Design and implement a Streamlit application where users can input eligibility criteria for placement. Based on these criteria, the application should query a dataset of student information to display eligible candidates' details.
# miniproject.ipynb
In this, I have imported necessary packages and created a database for Placement Eligibility and Created all the neccessary tables with column names mentioned in the documents.
Using faker created a list for each columns and loadded into the table
For all the Primary keys instead of integers, I have includents a pre-fix character for easy understanding.
Once after loading the data, I have alterred the table to set the foriegn key (I tried creating the foriegn key while creating the table in vscode but it throws Foriegn key constraint while loading. Hence Foriegn key created after loading the data. Alternatively I tried creating the database and tables in MySQL but felt this could be good way for practise and understanding)
# eligibleapp.py
In this using Streamlit, options are created in the sidebar and based on the selection list the queries pull the data from the table.
Also added Current date and time in some Tables which updates dynamically.
