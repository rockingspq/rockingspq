#!/usr/bin/env python
# coding: utf-8

# Below are the guidelines for the Project Notes-I:
# 
# Review Parameters	Points
# 1) Introduction of the business problem	4
# a) Defining problem statement	 
# b) Need of the study/project	 
# c) Understanding business/social opportunity	 
#  	 
# 2)Data Report	2
# a) Understanding how data was collected in terms of time, frequency and methodology	 
# b) Visual inspection of data (rows, columns, descriptive details)	 
# c) Understanding of attributes (variable info, renaming if required)	 
#  	 
# 3) Exploratory data analysis	10
# a) Univariate analysis (distribution and spread for every continuous attribute, distribution of data in categories for categorical ones)	 
# b) Bivariate analysis (relationship between different variables , correlations)	 
# a) Removal of unwanted variables (if applicable)	 
# b) Missing Value treatment (if applicable)	 
# d) Outlier treatment (if required)	 
# e) Variable transformation (if applicable)	 
# f) Addition of new variables (if required)	 
#  	 
# 4) Business insights from EDA 	4
# a) Is the data unbalanced? If so, what can be done? Please explain in the context of the business	 
# b) Any business insights using clustering  (if applicable)	 
# c) Any other business insights	 
#  	 
# Total	20

# In[426]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
import warnings
warnings.filterwarnings("ignore")


# In[427]:


df= pd.read_excel('Sports Data.xlsx',sheet_name='Sports data for DSBA')


# In[428]:


df.head(5)


# In[429]:


df.shape


# In[430]:


df.info()


# In[431]:


df['First_selection'].value_counts()


# In[432]:


df=df.replace(to_replace="Bat",value="Batting")


# In[433]:


df['First_selection'].value_counts()


# In[434]:


df['Result'].value_counts()


# In[435]:


df['Match_format'].value_counts()


# In[436]:


df=df.replace(to_replace ="20-20",value ="T20")


# In[437]:


df['Match_format'].value_counts()


# In[438]:


df['Match_light_type'].value_counts()


# In[439]:


df['Offshore'].value_counts()


# In[440]:


df.describe()


# In[441]:


df['Opponent'].value_counts()


# In[442]:


df['Season'].value_counts(normalize=True)*100


# In[443]:


df.dtypes


# In[444]:


df.info()


# In[445]:


df.isnull().sum()


# In[446]:


df.dtypes.value_counts()


# In[447]:


categoriacl_features=[]
numerical_features=[]
for i in df.columns:
    if df[i].dtype=="object":
        categoriacl_features.append(i)
    else:
        numerical_features.append(i)
print(categoriacl_features) 
print(numerical_features)


# ## Check for duplicate data

# In[448]:


dups = df.duplicated()
print('Number of duplicate rows = %d' % (dups.sum()))
df[dups]


# In[449]:


df.groupby(['Match_format',"Match_light_type",'Offshore','Result']).agg({'Result':'count'})


# In[450]:


df.groupby(['Opponent','Result']).agg({'Result':'count'})


# In[451]:


df.groupby(['Season','Result']).agg({'Result':'count'})


# In[452]:


df.groupby(['First_selection','Result']).agg({'Result':'count'})


# In[453]:


plt.figure(figsize=(10,8))
sns.distplot(df['Avg_team_Age'])


# In[454]:


plt.figure(figsize=(10,8))
sns.distplot(df['Bowlers_in_team'])


# In[455]:


plt.figure(figsize=(10,8))
sns.distplot(df['Extra_bowls_bowled'])


# In[456]:


plt.figure(figsize=(10,8))
sns.distplot(df['player_highest_run'])


# In[457]:


plt.figure(figsize=(10,8))
sns.distplot(df['Max_run_given_1over'])


# In[458]:


plt.figure(figsize=(10,8))
sns.distplot(df['Max_run_scored_1over'])


# In[459]:


plt.figure(figsize=(10,8))
sns.distplot(df['Max_wicket_taken_1over'])


# In[460]:


sns.countplot(df["Match_format"],hue=df["Result"]) 


# ## Outlier detection and treatment

# In[461]:


plt.figure(figsize=(15,15))
df[['Avg_team_Age', 'Bowlers_in_team', 'All_rounder_in_team','Max_run_scored_1over', 'Max_wicket_taken_1over', 'Extra_bowls_bowled', 'Min_run_given_1over', 'Min_run_scored_1over', 'Max_run_given_1over', 'extra_bowls_opponent', 'player_highest_run']].boxplot(vert=0)


# In[462]:


def remove_outlier(col):
    sorted(col)
    Q1,Q3=col.quantile([0.25,0.75])
    IQR=Q3-Q1
    lower_range= Q1-(1.5 * IQR)
    upper_range= Q3+(1.5 * IQR)
    return lower_range, upper_range 


# In[463]:


lrextra,urextra=remove_outlier(df['extra_bowls_opponent'])
df['extra_bowls_opponent']=np.where(df['extra_bowls_opponent']>urextra,urextra,df['extra_bowls_opponent'])
df['extra_bowls_opponent']=np.where(df['extra_bowls_opponent']<lrextra,lrextra,df['extra_bowls_opponent'])

lrextra1,urextra1=remove_outlier(df['Extra_bowls_bowled'])
df['Extra_bowls_bowled']=np.where(df['Extra_bowls_bowled']>urextra1,urextra1,df['Extra_bowls_bowled'])
df['Extra_bowls_bowled']=np.where(df['Extra_bowls_bowled']<lrextra1,lrextra1,df['Extra_bowls_bowled'])

lrmaxrun,urmaxrun=remove_outlier(df['Max_run_given_1over'])
df['Max_run_given_1over']=np.where(df['Max_run_given_1over']>urmaxrun,urmaxrun,df['Max_run_given_1over'])
df['Max_run_given_1over']=np.where(df['Max_run_given_1over']<lrmaxrun,lrmaxrun,df['Max_run_given_1over'])

lravg,uravg=remove_outlier(df['Avg_team_Age'])
df['Avg_team_Age']=np.where(df['Avg_team_Age']>uravg,uravg,df['Avg_team_Age'])
df['Avg_team_Age']=np.where(df['Avg_team_Age']<lravg,lravg,df['Avg_team_Age'])

df.shape


# In[464]:


plt.figure(figsize=(15,15))
df[['Avg_team_Age', 'Bowlers_in_team', 'All_rounder_in_team','Max_run_scored_1over', 'Max_wicket_taken_1over', 'Extra_bowls_bowled', 'Min_run_given_1over', 'Min_run_scored_1over', 'Max_run_given_1over', 'extra_bowls_opponent', 'player_highest_run']].boxplot(vert=0)


# ## Dropping Audience Number

# In[465]:


df.drop('Audience_number',axis=1,inplace=True)
df.drop('Wicket_keeper_in_team',axis=1,inplace=True)


# In[466]:


df.head(2).transpose()


# ## Check for Missing Value

# In[467]:


df.isnull().sum()[df.isnull().sum()>0]


# In[468]:


df[df.isnull().sum()[df.isnull().sum()>0].index].dtypes


# In[469]:


median1=df["Avg_team_Age"].median()
median2=df["Bowlers_in_team"].median()
median3=df["All_rounder_in_team"].median()
median4=df["Max_run_scored_1over"].median()


df["Avg_team_Age"].replace(np.nan,median1,inplace=True)
df["Bowlers_in_team"].replace(np.nan,median2,inplace=True)
df["All_rounder_in_team"].replace(np.nan,median3,inplace=True)
df["Max_run_scored_1over"].replace(np.nan,median4,inplace=True)
                    


# In[470]:


median5=df["Extra_bowls_bowled"].median()
median6=df["Min_run_scored_1over"].median()
median7=df["Max_run_given_1over"].median()
median8=df["player_highest_run"].median()


df["Extra_bowls_bowled"].replace(np.nan,median5,inplace=True)
df["Min_run_scored_1over"].replace(np.nan,median6,inplace=True)
df["Max_run_given_1over"].replace(np.nan,median7,inplace=True)
df["player_highest_run"].replace(np.nan,median8,inplace=True) 


# In[471]:


df[df.isnull().sum()[df.isnull().sum()>0].index].dtypes


# In[472]:


mode1=df['Match_light_type'].mode().values[0]
mode2=df["Match_format"].mode().values[0]
mode3=df["First_selection"].mode().values[0]
mode4=df["Opponent"].mode().values[0]
mode5=df["Season"].mode().values[0]
mode6=df['Offshore'].mode().values[0]



df["Match_light_type"]=df["Match_light_type"].replace(np.nan,mode1)
df["Match_format"]= df["Match_format"].replace(np.nan,mode2)
df["First_selection"]=df["First_selection"].replace(np.nan,mode3)
df["Opponent"]=df["Opponent"].replace(np.nan,mode4)
df["Season"]=df["Season"].replace(np.nan,mode5)
df["Offshore"]=df["Offshore"].replace(np.nan,mode6)


# In[473]:


imp_factor=df[['Avg_team_Age','Bowlers_in_team','All_rounder_in_team', 'Max_run_scored_1over', 'Max_wicket_taken_1over', 'Extra_bowls_bowled', 'Min_run_given_1over', 'Min_run_scored_1over', 'Max_run_given_1over', 'extra_bowls_opponent']]


# In[474]:


sns.pairplot(imp_factor)


# # check correlation among the features

# In[475]:


plt.figure(figsize=(15,15))
sns.heatmap(imp_factor.corr(), annot=True,cmap='Blues')


# In[ ]:




