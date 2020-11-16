#!/usr/bin/env python
# coding: utf-8

# # Homework 6, Part Two: A dataset about dogs.
# 
# Data from [a FOIL request to New York City](https://www.muckrock.com/foi/new-york-city-17/pet-licensing-data-for-new-york-city-23826/)

# ## Do your importing and your setup

# In[1]:


import pandas as pd
import numpy as np
pd.set_option("display.max_columns", 200)
pd.set_option("display.max_colwidth", 200)


# ## Read in the file `NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx` and look at the first five rows

# In[2]:


df = pd.read_excel("NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx", nrows=30000, na_values=["Unknown", "UNKNOWN"])
df.head()


# ## How many rows do you have in the data? What are the column types?
# 
# If there are more than 30,000 rows in your dataset, go back and only read in the first 30,000.

# In[3]:


df.shape


# In[4]:


df.dtypes


# ## Describe the dataset in words. What is each row? List two column titles along with what each of those columns means.
# 
# For example: “Each row is an animal in the zoo. `is_reptile` is whether the animal is a reptile or not”

# Each row is a dog that has a license associated with it. Animal Name is the dog's name, and Primary Breed is the dog's main, most dominant breed.

# # Your thoughts
# 
# Think of four questions you could ask this dataset. **Don't ask them**, just write them down in the cell below. Feel free to use either Markdown or Python comments.

# What is the most common type(breed) of dog in this dataset?
# How many dogs in the dataset have been spayed or neutered?
# How many licenses will expire before the end of 2016?
# How many dogs have been trained?

# # Looking at some dogs

# ## What are the most popular (primary) breeds of dogs? Graph the top 10.

# In[5]:


df.columns = df.columns.str.strip().str.replace(' ', '_')
# df.head()
df.Primary_Breed.value_counts().sort_values(ascending=False).head(10)
#df.Primary_Breed.value_counts().head(10).plot(figsize=(10, 10), kind='barh')


# ## "Unknown" is a terrible breed! Graph the top 10 breeds that are NOT Unknown

# In[6]:


df.Primary_Breed.value_counts().head(10).sort_values(ascending=True).plot(figsize=(10, 10), kind='barh')


# ## What are the most popular dog names?

# In[7]:


df.Animal_Name.value_counts().head().to_frame().reset_index()


# ## Do any dogs have your name? How many dogs are named "Max," and how many are named "Maxwell"?

# In[8]:


df[df.Animal_Name == 'Sheridan']
# No dogs with my name


# In[9]:


len(df[df.Animal_Name == 'Max'])


# In[10]:


len(df[df.Animal_Name == 'Maxwell'])


# ## What percentage of dogs are guard dogs?
# 
# Check out the documentation for [value counts](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.value_counts.html).

# In[11]:


df.Guard_or_Trained.value_counts(normalize=True)*100


# ## What are the actual numbers?

# In[12]:


df.Guard_or_Trained.value_counts()


# ## Wait... if you add that up, is it the same as your number of rows? Where are the other dogs???? How can we find them??????
# 
# Use your `.head()` to think about it, then you'll do some magic with `.value_counts()`

# In[13]:


df.Guard_or_Trained.value_counts(dropna=False)


# ## Fill in all of those empty "Guard or Trained" columns with "No"
# 
# Then check your result with another `.value_counts()`

# In[14]:


df.Guard_or_Trained = df.Guard_or_Trained.replace({
  np.nan:"No"
})
df.Guard_or_Trained.value_counts()


# ## What are the top dog breeds for guard dogs? 

# In[15]:


guard_dogs= df[df.Guard_or_Trained == 'Yes']
guard_dogs.Primary_Breed.value_counts().head(5).reset_index()


# ## Create a new column called "year" that is the dog's year of birth
# 
# The `Animal Birth` column is a datetime, so you can get the year out of it with the code `df['Animal Birth'].apply(lambda birth: birth.year)`.

# In[16]:


df["Year"] = df['Animal_Birth'].apply(lambda birth: birth.year)
df.head()


# ## Calculate a new column called “age” that shows approximately how old the dog is. How old are dogs on average?

# In[17]:


df['Age'] = 2020 - df['Year']
df.head()


# # Joining data together

# In[18]:


# pd.merge to combine dataframes
# dataframe.merge(other_dataframe)
# left_on="" (left most dataframe), right_on=""
# how = "left, right, outer or inner"
        # Outer allows you to join things without an exact match
        # Left keeps everything without a match to the left and vice versa


# ## Which neighborhood does each dog live in?
# 
# You also have a (terrible) list of NYC neighborhoods in `zipcodes-neighborhoods.csv`. Join these two datasets together, so we know what neighborhood each dog lives in. **Be sure to not read it in as `df`, or else you'll overwrite your dogs dataframe.**

# In[31]:


neighborhoods = pd.read_csv("zipcodes-neighborhoods.csv", nrows=30000, na_values=["Unknown", "UNKNOWN", "unknown"])
neighborhoods.head()
dogs = df.merge(neighborhoods,
                how='left',
                left_on="Owner_Zip_Code",
                right_on="zip")
dogs


# ## What is the most popular dog name in all parts of the Bronx? How about Brooklyn? The Upper East Side?

# In[32]:


bronx_dogs = dogs[dogs.borough == 'Bronx']
bronx_dogs.Animal_Name.value_counts().head()


# In[34]:


brooklyn_dogs = dogs[dogs.borough == "Brooklyn"]
brooklyn_dogs.Animal_Name.value_counts().head()


# In[22]:


UWS_dogs = dogs[dogs.neighborhood == 'Upper West Side']
UWS_dogs.Animal_Name.value_counts().head()


# ## What is the most common dog breed in each of the neighborhoods of NYC?

# In[47]:


dogs.groupby(by='neighborhood').Primary_Breed.value_counts().sort_values(ascending=False)
# OR dogs.groupby(by='neighborhood').Primary_Breed.value_counts().groupby(level=0).nlargest(5)
# But the above prints the neighborhoods twice


# In[ ]:





# ## What breed of dogs are the least likely to be spayed? Male or female?

# In[24]:


non_spayed_dogs = dogs[dogs.Spayed_or_Neut == 'No']
non_spayed_dogs.Primary_Breed.value_counts().head(10) # --> Yorkshire Terriers are least likely to be spayed
non_spayed_dogs.Animal_Gender.value_counts() # --> male dogs are least likely to be neutered
# How do I find which gender of the above selected dogs are least likely to be spayed?


# ## Make a new column called monochrome that is True for any animal that only has black, white or grey as one of its colors. How many animals are monochrome?

# In[25]:


# dogs = dogs.Animal_Dominant_Color.replace({
#     'White' : 'WHITE',
#     'Black' : 'BLACK',
#     'Grey' : 'GREY',
#     'Gray' : 'GREY',
#     'GRAY' : 'GREY'
# })
# dogs = dogs.Animal_Secondary_Color.replace({
#     'White' : 'WHITE',
#     'Black' : 'BLACK',
#     'Grey' : 'GREY',
#     'Gray' : 'GREY',
#     'GRAY' : 'GREY'
# })
# dogs = dogs.Animal_Third_Color.replace({
#     'White' : 'WHITE',
#     'Black' : 'BLACK',
#     'Grey' : 'GREY',
#     'Gray' : 'GREY',
#     'GRAY' : 'GREY'
# })


# In[26]:


# dogs['Monochrome'] = 


# In[ ]:





# In[ ]:





# ## How many dogs are in each borough? Plot it in a graph.

# In[27]:


dogs.borough.value_counts()
dogs.borough.value_counts().plot(kind='barh')


# ## Which borough has the highest number of dogs per-capita?
# 
# You’ll need to merge in `population_boro.csv`

# In[28]:


boroughs = pd.read_csv("boro_population.csv", nrows=30000)
boroughs.head()
populations = dogs.merge(boroughs,
                         how='left',
                         left_on='borough',
                         right_on='borough')


# In[70]:


#dogs per capita = # of dogs/population * 1000
# # of dogs/population * 1000 ---> There are this many dogs per thousand people
Manhattan = populations[populations.borough == "Manhattan"]
print(round((len(Manhattan)/Manhattan.population.max())*1000))

Brooklyn = populations[populations.borough == "Brooklyn"]
print(round((len(Brooklyn)/Brooklyn.population.max())*1000))

Bronx = populations[populations.borough == "Bronx"]
print(round((len(Bronx)/Bronx.population.max())*1000))

Queens = populations[populations.borough == "Queens"]
print(round((len(Queens)/Queens.population.max())*1000))

Staten_Island = populations[populations.borough == "Staten Island"]
print(round((len(Staten_Island)/Staten_Island.population.max())*1000))

#Manhattan & Staten_Island have most dogs per capita


# ## Make a bar graph of the top 5 breeds in each borough.
# 
# How do you groupby and then only take the top X number? You **really** should ask me, because it's kind of crazy.

# In[66]:


top_breeds = populations.groupby('borough').Primary_Breed.value_counts().groupby(level=0).nlargest(5).plot(figsize=(10,20), kind='barh')
top_breeds


# ## What percentage of dogs are not guard dogs?

# In[68]:


not_guard = populations[populations.Guard_or_Trained == 'No']
len(not_guard)/len(populations)*100


# In[ ]:




