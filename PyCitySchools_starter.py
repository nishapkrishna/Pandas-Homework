#!/usr/bin/env python
# coding: utf-8

# # PyCity Schools Analysis
# 
# * As a whole, schools with higher budgets, did not yield better test results. By contrast, schools with higher spending per student actually (\$645-675) underperformed compared to schools with smaller budgets (<\$585 per student).
# 
# * As a whole, smaller and medium sized schools dramatically out-performed large sized schools on passing math performances (89-91% passing vs 67%).
# 
# * As a whole, charter schools out-performed the public district schools across all metrics. However, more analysis will be required to glean if the effect is due to school practices or the fact that charter schools tend to serve smaller student populations per school. 
# ---

# ### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[2]:


# Dependencies and Setup
import pandas as pd
import numpy as np

# File to Load (Remember to Change These)
school_data_to_load = "Resources/schools_complete.csv"
student_data_to_load = "Resources/students_complete.csv"

# Read School and Student Data File and store into Pandas Data Frames
school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)

# Combine the data into a single dataset
school_data_complete = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])


# ## District Summary
# 
# * Calculate the total number of schools
# 
# * Calculate the total number of students
# 
# * Calculate the total budget
# 
# * Calculate the average math score 
# 
# * Calculate the average reading score
# 
# * Calculate the overall passing rate (overall average score), i.e. (avg. math score + avg. reading score)/2
# 
# * Calculate the percentage of students with a passing math score (70 or greater)
# 
# * Calculate the percentage of students with a passing reading score (70 or greater)
# 
# * Create a dataframe to hold the above results
# 
# * Optional: give the displayed data cleaner formatting

# In[3]:


# Calculating the total number of schools
Total_School = len(school_data_complete["School ID"].unique())

# Calculating the total number of students
Total_Students = school_data_complete["Student ID"].count()

# Calculating the total budget
Total_Budget = school_data["budget"].sum()

# Calculating the average math score
Math_Avg = student_data["math_score"].mean()

# Calculating the average reading score
Reading_Avg = student_data["reading_score"].mean()

# Calculating the overall passing rate
Passing_Rate = (Math_Avg + Reading_Avg) / 2

# Calculating the percentage of students with a passing math score (70 or greater)
Math_Passing_Score = school_data_complete[(school_data_complete["math_score"] >= 70)].count()["student_name"]
Math_Pass_Percentage = Math_Passing_Score / float(Total_Students) * 100

# Calculating the percentage of students with a passing reading score (70 or greater)
Reading_Passing_Score = school_data_complete[(school_data_complete["reading_score"] >= 70)].count()["student_name"]
Read_Pass_Percentage = Reading_Passing_Score / float(Total_Students) * 100

# Creating a dataframe to hold the results
District_Summary = pd.DataFrame({"Total Schools" : [Total_School],
                                 "Total Students" : [Total_Students],
                                 "Total Budget" : [Total_Budget],
                                 "Average Math Score" : [Math_Avg],
                                 "Average Rading Score" : [Reading_Avg],
                                 "% Passing Math" : [Math_Pass_Percentage],
                                 "% Passing Reading" : [Read_Pass_Percentage],
                                 "% Overall Passing Rate" : [Passing_Rate]})
District_Summary = District_Summary[["Total Schools","Total Students","Total Budget",
                                    "Average Math Score","Average Rading Score",
                                    "% Passing Math","% Passing Reading",
                                    "% Overall Passing Rate"]]

# Change the format for total students and total budget 
District_Summary["Total Students"] = District_Summary["Total Students"].map("{:,}".format)
District_Summary["Total Budget"] = District_Summary["Total Budget"].map("${:,.2f}".format)

# Display the District summary
District_Summary


# ## School Summary

# * Create an overview table that summarizes key metrics about each school, including:
#   * School Name
#   * School Type
#   * Total Students
#   * Total School Budget
#   * Per Student Budget
#   * Average Math Score
#   * Average Reading Score
#   * % Passing Math
#   * % Passing Reading
#   * Overall Passing Rate (Average of the above two)
#   
# * Create a dataframe to hold the above results

# In[6]:


# Finding school type
school_types = school_data.set_index(["school_name"])["type"]

# Total students for each school
Total_Students = school_data_complete["school_name"].value_counts()

# Total School Budget
School_Budget = school_data.groupby(["school_name"]).mean()["budget"]

# Per Student Budget
Student_Budget = School_Budget / Total_Students

# Average Math Score
Avg_Math_Score = school_data_complete.groupby(["school_name"]).mean()["math_score"] 

# Average Reading Score
Avg_Read_Score = school_data_complete.groupby(["school_name"]).mean()["reading_score"]

# % Passing Math
Pass_Math = school_data_complete[(school_data_complete["math_score"] >= 70)]
Sch_Pass_math = Pass_Math.groupby(["school_name"]).count()["student_name"] / Total_Students * 100

# % Passing Reading
Pass_Reading = school_data_complete[(school_data_complete["reading_score"] >= 70)]
Sch_Pass_Reading = Pass_Reading.groupby(["school_name"]).count()["student_name"] / Total_Students * 100

# Overall Passing Rate
Overall_Pass = (Sch_Pass_math + Sch_Pass_Reading) /2 

# Creating a dataframe to hold the results
School_Summary = pd.DataFrame({"School Type": school_types,
                               "Total Students": Total_Students,
                               "Total School Budget" : School_Budget,
                               "Per Student Budget" : Student_Budget,
                               "Average Math Score" : Avg_Math_Score,
                               "Average Reading Score" : Avg_Read_Score,
                               "% Passing Math" : Sch_Pass_math,
                               "% Passing Reading" : Sch_Pass_Reading,
                               "% Overall Passing Rate" : Overall_Pass})

School_Summary = School_Summary[["School Type",
                                 "Total Students",
                                 "Total School Budget",
                                 "Per Student Budget",
                                 "Average Math Score",
                                 "Average Reading Score",
                                 "% Passing Math",
                                 "% Passing Reading",
                                 "% Overall Passing Rate"]]

# Change the format for total school budget and student budget
School_Summary["Total School Budget"] = School_Summary["Total School Budget"].map("${:,.2f}".format)
School_Summary["Per Student Budget"] = School_Summary["Per Student Budget"].map("${:,.2f}".format)

# Display the school summary
School_Summary


# ## Top Performing Schools (By Passing Rate)

# * Sort and display the top five schools in overall passing rate

# In[7]:


# Sort and display the top five schools in overall passing rate

Top_Performing_schools = School_Summary.sort_values("% Overall Passing Rate", ascending = False)
Top_Performing_schools.head()


# ## Bottom Performing Schools (By Passing Rate)

# * Sort and display the five worst-performing schools

# In[8]:


# Sort and display the five worst-performing schools

Bottom_Performing_schools = School_Summary.sort_values("% Overall Passing Rate")
Bottom_Performing_schools.head()


# ## Math Scores by Grade

# * Create a table that lists the average Reading Score for students of each grade level (9th, 10th, 11th, 12th) at each school.
# 
#   * Create a pandas series for each grade. Hint: use a conditional statement.
#   
#   * Group each series by school
#   
#   * Combine the series into a dataframe
#   
#   * Optional: give the displayed data cleaner formatting

# In[9]:


# Creating a pandas series for each grade

nineth_graders = student_data[(student_data["grade"] == "9th")]
tenth_graders = student_data[(student_data["grade"] == "10th")]
eleventh_graders = student_data[(student_data["grade"] == "11th")]
twelfth_graders = student_data[(student_data["grade"] == "12th")]

# Group each series by school

nineth_graders_scores = nineth_graders.groupby(["school_name"]).mean()["math_score"]
tenth_graders_scores = tenth_graders.groupby(["school_name"]).mean()["math_score"]
eleventh_graders_scores = eleventh_graders.groupby(["school_name"]).mean()["math_score"]
twelfth_graders_scores = twelfth_graders.groupby(["school_name"]).mean()["math_score"]

# Combine the series into a dataframe

Math_Grade_df = pd.DataFrame({"9th" : nineth_graders_scores, "10th" : tenth_graders_scores,
                              "11th" : eleventh_graders_scores, "12th" : twelfth_graders_scores})


Math_Grade_df.index.name = None
Math_Grade_df


# ## Reading Score by Grade 

# * Perform the same operations as above for reading scores

# In[10]:


# Creating a pandas series for each grade

nineth_graders_reading = student_data[(student_data["grade"] == "9th")]
tenth_graders_reading = student_data[(student_data["grade"] == "10th")]
eleventh_graders_reading = student_data[(student_data["grade"] == "11th")]
twelfth_graders_reading = student_data[(student_data["grade"] == "12th")]

# Group each series by school

nineth_reading_scores = nineth_graders_reading.groupby(["school_name"]).mean()["reading_score"]
tenth_reading_scores = tenth_graders_reading.groupby(["school_name"]).mean()["reading_score"]
eleventh_reading_scores = eleventh_graders_reading.groupby(["school_name"]).mean()["reading_score"]
twelfth_reading_scores = twelfth_graders_reading.groupby(["school_name"]).mean()["reading_score"]

# Combine the series into a dataframe
Reading_Grade_df = pd.DataFrame({"9th" : nineth_reading_scores, "10th" : tenth_reading_scores,
                              "11th" : eleventh_reading_scores, "12th" : twelfth_reading_scores})


Reading_Grade_df.index.name = None
Reading_Grade_df


# ## Scores by School Spending

# * Create a table that breaks down school performances based on average Spending Ranges (Per Student). Use 4 reasonable bins to group school spending. Include in the table each of the following:
#   * Average Math Score
#   * Average Reading Score
#   * % Passing Math
#   * % Passing Reading
#   * Overall Passing Rate (Average of the above two)

# In[12]:


# Sample bins. Feel free to create your own bins.
spending_bins = [0, 585, 615, 645, 675]
group_names = ["<$585", "$585-615", "$615-645", "$645-675"]


# In[13]:


# Creating a table that breaks down school performances based on average Spending Ranges (Per Student)
School_Summary["Spending Ranges(Per Student)"] = pd.cut(Student_Budget,spending_bins, labels = group_names)

# Average Math Score
School_Avg_Math = School_Summary.groupby(["Spending Ranges(Per Student)"]).mean()["Average Math Score"]

# Average Reading Score
School_Avg_Reading = School_Summary.groupby(["Spending Ranges(Per Student)"]).mean()["Average Reading Score"]

# % Passing Math
Per_Pass_Math = School_Summary.groupby(["Spending Ranges(Per Student)"]).mean()["% Passing Math"]

# % Passing Reading
Per_Pass_Reading = School_Summary.groupby(["Spending Ranges(Per Student)"]).mean()["% Passing Reading"]

# Overall Passing Rate
Over_Pass_Rate = (Per_Pass_Math + Per_Pass_Reading) / 2

# Combine the series into a dataframe
Score_School_Spending = pd.DataFrame({"Average Math Score" : School_Avg_Math,
                                      "Average Reading Score" : School_Avg_Reading,
                                      "% Passing Math" : Per_Pass_Math,
                                      "% Passing Reading" : Per_Pass_Reading,
                                      "% Overall Passing Rate" : Over_Pass_Rate})

# Display Scores by school pending
Score_School_Spending


# ## Scores by School Size

# * Perform the same operations as above, based on school size.

# In[14]:


# Sample bins. Feel free to create your own bins.

size_bins = [0, 1000, 2000, 5000]
group_names = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]


# In[15]:


# Creating a table that breaks down school performances based on school size
School_Summary["School Size"] = pd.cut(Total_Students,size_bins, labels = group_names)


# Average Math Score
School_Avg_Math = School_Summary.groupby(["School Size"]).mean()["Average Math Score"]

# Average Reading Score
School_Avg_Reading = School_Summary.groupby(["School Size"]).mean()["Average Reading Score"]

# % Passing Math
Per_Pass_Math = School_Summary.groupby(["School Size"]).mean()["% Passing Math"]

# % Passing Reading
Per_Pass_Reading = School_Summary.groupby(["School Size"]).mean()["% Passing Reading"]

# Overall Passing Rate
Over_Pass_Rate = (Per_Pass_Math + Per_Pass_Reading) / 2

# Combine the series into a dataframe
Score_School_Size = pd.DataFrame({"Average Math Score" : School_Avg_Math,
                                      "Average Reading Score" : School_Avg_Reading,
                                      "% Passing Math" : Per_Pass_Math,
                                      "% Passing Reading" : Per_Pass_Reading,
                                      "% Overall Passing Rate" : Over_Pass_Rate})

# Display the scores by school size
Score_School_Size


# ## Scores by School Type

# * Perform the same operations as above, based on school type.

# In[16]:


#Creating a table that breaks down school performances based on school type.

School_Avg_Math = School_Summary.groupby(["School Type"]).mean()["Average Math Score"]

School_Avg_Reading = School_Summary.groupby(["School Type"]).mean()["Average Reading Score"]

Per_Pass_Math = School_Summary.groupby(["School Type"]).mean()["% Passing Math"]

Per_Pass_Reading = School_Summary.groupby(["School Type"]).mean()["% Passing Reading"]

Over_Pass_Rate = (Per_Pass_Math + Per_Pass_Reading) / 2

# Combine the series into a dataframe
School_Type = pd.DataFrame({"Average Math Score" : School_Avg_Math,
                                      "Average Reading Score" : School_Avg_Reading,
                                      "% Passing Math" : Per_Pass_Math,
                                      "% Passing Reading" : Per_Pass_Reading,
                                      "% Overall Passing Rate" : Over_Pass_Rate})

# Display scores by school type
School_Type


# In[ ]:




