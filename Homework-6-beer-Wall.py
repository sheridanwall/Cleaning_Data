#!/usr/bin/env python
# coding: utf-8

# # Homework 6, Part One: Lots and lots of questions about beer

# ### Do your importing and your setup

# In[1]:


import pandas as pd


# ## Read in the file `craftcans.csv`, and look at the first first rows

# In[2]:


df = pd.read_csv("craftcans.csv", na_values='Does not apply')
df.head()


# ## How many rows do you have in the data? What are the column types?

# In[3]:


df.describe()


# In[4]:


df.shape


# In[5]:


df.dtypes


# # Checking out our alcohol

# ## What are the top 10 producers of cans of beer?

# In[6]:


df.head()


# In[7]:


df.Brewery.value_counts().head(10)


# ## What is the most common ABV? (alcohol by volume)

# In[8]:


df.ABV.mode()


# ## Oh, weird, ABV isn't a number. Convert it to a number for me, please.
# 
# It's going to take a few steps!
# 
# ### First, let's just look at the ABV column by itself

# In[9]:


df.ABV.head()


# ### Hm, `%` isn't part of  a number. Let's remove it.
# 
# When you're confident you got it right, save the results back into the `ABV` column.
# 
# - *Tip: In programming the easiest way to remove something is to *replacing it with nothing*.
# - *Tip: "nothing" might seem like `NaN` sinc we talked about it a lot in class, but in this case it isn't! It's just an empty string, like ""*
# - *Tip: `.replace` is used for replacing ENTIRE cells, while `.str.replace` is useful for replacing PARTS of cells (see my New York example)*

# In[10]:


df.ABV.str.replace('%', '', n=-1, case=None, regex=True)
df.ABV=df.ABV.str.replace('%', '', n=-1, case=None, regex=True)


# ### Now let's turn `ABV` into a numeric data type
# 
# Save the results back into the `ABV` column (again), and then check `df.dtypes` to make sure it worked.
# 
# - *Tip: We used `.astype(int)` during class, but this has a decimal in it...*

# In[11]:


df.ABV.astype(float)
df.ABV=df.ABV.astype(float)
df.head()
df.dtypes


# ## What's the ABV of the average beer look like?
# 
# ### Show me in two different ways: one command to show the `median`/`mean`/etc, and secondly show me a chart

# In[12]:


df.ABV.median()
df.describe()


# In[13]:


df.ABV.hist()


# ### We don't have ABV for all of the beers, how many are we missing them from?
# 
# - *Tip: You can use `isnull()` or `notnull()` to see where a column is missing data.*
# - *Tip: You just want to count how many `True`s and `False`s there are.*
# - *Tip: It's a weird trick involving something we usually use to count things in a column*

# In[14]:


df.ABV.isnull().value_counts()


# # Looking at location
# 
# Brooklyn used to produce 80% of the country's beer! Let's see if it's still true.

# ## What are the top 10 cities in the US for canned craft beer?

# In[15]:


df.Location.value_counts().head(10)


# ## List all of the beer from Brooklyn, NY

# In[16]:


brooklyn = df[df.Location == 'Brooklyn, NY']
brooklyn.Beer


# ## What brewery in Brooklyn puts out the most cans of beer?

# In[17]:


brooklyn.Brewery.value_counts().head(1)


# ## What are the five most popular styles of beer produced by Sixpoint?

# In[18]:


sixpoint = df[df.Brewery == 'Sixpoint Craft Ales']
sixpoint.Style.value_counts().head(5)


# ## List all of the breweries in New York state.
# 
# - *Tip: We want to match *part* of the `Location` column, but not all of it.*
# - *Tip: Watch out for `NaN` values! You might be close, but you'll need to pass an extra parameter to make it work without an error.*

# In[19]:


df.dropna(subset = ['Location'])
df = df.dropna(subset = ['Location'])


# ### Now *count* all of the breweries in New York state

# In[20]:


new_york = df[df.Location.str.contains("NY")]
new_york.Brewery.value_counts().sum()


# # Measuring International Bitterness Units
# 
# ## Display all of the IPAs
# 
# Include American IPAs, Imperial IPAs, and anything else with "IPA in it."
# 
# IPA stands for [India Pale Ale](https://www.bonappetit.com/story/ipa-beer-styles), and is probably the most popular kind of beer in the US for people who are drinking [craft beer](https://www.craftbeer.com/beer/what-is-craft-beer).

# In[21]:


df.dropna(subset = ['Style'])
df = df.dropna(subset = ['Style'])
IPA = df[df.Style.str.contains("IPA")]
IPA


# IPAs are usually pretty hoppy and bitter. IBU stands for [International Bitterness Unit](http://www.thebrewenthusiast.com/ibus/), and while a lot of places like to brag about having the most bitter beer (it's an American thing!), IBUs don't necessary *mean anything*.
# 
# Let's look at how different beers have different IBU measurements.

# ## Try to get the average IBU measurement across all beers

# In[22]:


df.IBUs.mean()


# ### Oh no, it doesn't work!
# 
# It looks like some of those values *aren't numbers*. There are two ways to fix this:
# 
# 1. Do the `.replace` and `np.nan` thing we did in class. Then convert the column to a number. This is boring.
# 2. When you're reading in your csv, there [is an option called `na_values`](http://pandas.pydata.org/pandas-docs/version/0.23/generated/pandas.read_csv.html). You can give it a list of **numbers or strings to count as `NaN`**. It's a lot easier than doing the `np.nan` thing, although you'll need to go add it up top and run all of your cells again.
# 
# - *Tip: Make sure you're giving `na_values` a LIST, not just a string*
# 
# ### Now try to get the average IBUs again

# In[23]:


df.IBUs.mean()


# ## Draw the distribution of IBU measurements, but with *twenty* bins instead of the default of 10
# 
# - *Tip: Every time I ask for a distribution, I'm looking for a histogram*
# - *Tip: Use the `?` to get all of the options for building a histogram*
# - *Tip: Make sure your `matplotlib` thing is set up right!*

# In[24]:


df.IBUs.hist(bins=20)


# ## Hm, Interesting distribution. List all of the beers with IBUs above the 75th percentile
# 
# - *Tip: There's a single that gives you the 25/50/75th percentile*
# - *Tip: You can just manually type the number when you list those beers*

# In[25]:


df.describe()


# In[26]:


IBU_75 = df[df.IBUs > 75.0]
IBU_75.Beer


# ## List all of the beers with IBUs below the 25th percentile

# In[27]:


IBU_25 = df[df.IBUs < 25.0]
IBU_25.Beer


# ## List the median IBUs of each type of beer. Graph it.
# 
# Put the highest at the top, and the missing ones at the bottom.
# 
# - Tip: Look at the options for `sort_values` to figure out the `NaN` thing. The `?` probably won't help you here.

# In[28]:


IBUs_median = df.groupby('Style').IBUs.median()
IBUs_median


# In[29]:


df.groupby('Style').IBUs.median().sort_values(ascending=True, na_position='first').plot(x='Beer', y='IBUs', figsize=(10,25), kind='barh')


# My Jupyter Notebook thinks it's opposite day. Why does ascending=True order it highest to lowest and na_position='first' move the nulls to the bottom?

# ## Hmmmm, it looks like they are generally different styles. What are the most common 5 styles of high-IBU beer vs. low-IBU beer?
# 
# - *Tip: You'll want to think about it in three pieces - filtering to only find the specific beers beers, then finding out what the most common styles are, then getting the top 5.*
# - *Tip: You CANNOT do this in one command. It's going to be one command for the high and one for the low.*
# - *Tip: "High IBU" means higher than 75th percentile, "Low IBU" is under 25th percentile*

# In[30]:


high_IBU = IBU_75.Style.value_counts().head(5)
high_IBU


# In[31]:


low_IBU = IBU_25.Style.value_counts().head(5)
low_IBU


# ## Get the average IBU of "Witbier", "Hefeweizen" and "American Pale Wheat Ale" styles
# 
# I'm counting these as wheat beers. If you see any other wheat beer categories, feel free to include them. I want ONE measurement and ONE graph, not three separate ones. And 20 to 30 bins in the histogram, please.
# 
# - *Tip: I hope that `isin` is in your toolbox*

# In[47]:


IBU_wheats = df["Style"].isin(["Witbier", "Hefeweizen", "American Pale Wheat Ale" ]) 
df[IBU_wheats].IBUs.mean()


# ## Draw a histogram of the IBUs of those beers

# In[48]:


df[IBU_wheats].IBUs.hist(bins=30)


# ## Get the average IBU of any style with "IPA" in it (also draw a histogram)

# In[49]:


IBU_IPA = df[df.Style.str.contains("IPA")]
IBU_IPA.IBUs.mean()


# In[50]:


IBU_IPA.IBUs.hist(bins=30)


# ## Plot those two histograms on top of one another
# 
# To plot two plots on top of one another, you do two steps.
# 
# 1. First, you make a plot using `plot` or `hist`, and you save it into a variable called `ax`.
# 2. You draw your second graph using `plot` or `hist`, and send `ax=ax` to it as a parameter.
# 
# It would look something like this:
# 
# ```python
# ax = df.plot(....)
# df.plot(ax=ax, ....)
# ``` 
# 
# (...except totally different)

# In[75]:


ax = df[IBU_wheats].IBUs.hist(bins=30)
IBU_IPA.IBUs.hist(ax=ax, bins=30)


# ## Compare the ABV of wheat beers vs. IPAs : their IBUs were really different, but how about their alcohol percentage?
# 
# Wheat beers might include witbier, hefeweizen, American Pale Wheat Ale, and anything else you think is wheaty. IPAs probably have "IPA" in their name.

# In[59]:


ABV_wheats = df["Style"].isin(["Witbier", "Hefeweizen", "American Pale Wheat Ale" ]) 
df[ABV_wheats].ABV.mean()


# In[60]:


ABV_IPA = df[df.Style.str.contains("IPA")]
ABV_IPA.ABV.mean()


# Are we supposed to make a graph to compare here like the one in the above question?

# In[78]:


ax = df[ABV_wheats].ABV.hist(bins=30)
ABV_IPA.ABV.hist(ax=ax, bins=30)


# ## Good work!
# 
# If you made it this far you deserve a drink.

# Yes, I do!
