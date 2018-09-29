
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import io

import numpy as np 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys

# using Basemap for map visualization. Installed it with "conda install basemap"
from mpl_toolkits.basemap import Basemap
from matplotlib import animation, rc
import warnings
warnings.filterwarnings('ignore')


# In[2]:


worldCities = pd.read_csv("./world-cities.csv", encoding='latin1')
# worldCities.head()


# In[3]:


dip = pd.read_csv("./diplomaticPosting.tsv", sep="\t")
# dip.head()


# In[4]:


dip.location.replace("U.S.A.", "United States", inplace=True)
dip.location.replace("U.S.S.R.", "Russia", inplace=True)

dip.location.replace("Bosnia Herzegovina", "Bosnia and Herzegovina", inplace=True)
dip.location.replace("Bosnia-Herzegovina", "Bosnia and Herzegovina", inplace=True)
dip.location.replace("Buda-Pest", "Budapest", inplace=True)
dip.location.replace("Camboadia", "Cambodia", inplace=True)

dip.location.replace('China (Counsellor)', 'China', inplace=True)
dip.location.replace('China, 1912', 'China', inplace=True)
dip.location.replace('Israel (did not proceed)', 'Israel', inplace=True)
dip.location.replace('Morocco (Rabat)', 'Morocco', inplace=True)
dip.location.replace('Russia (Counsellor)', 'Russia', inplace=True)
dip.location.replace('Sir Lanka', "Sri Lanka", inplace=True)
dip.location.replace("Tanganykia", "Tanzania", inplace=True)
dip.location.replace('The Netherlands', "Netherlands", inplace=True)
dip.location.replace('Zaire' "Democratic Republic of Congo", inplace=True)
dip.location.replace("Rhodesia", "Zimbabwe", inplace=True)
dip.location.replace("Southern Rhodesia", "Zimbabwe", inplace=True)
dip.location.replace("Northern Rhodesia", "Zimbabwe", inplace=True)


# In[5]:


# np.unique(dip.location.values.astype(str))


# In[6]:


known_countries = np.unique(worldCities.country.tolist())
known_cities = np.unique(worldCities["name"].tolist())


# In[7]:


# known_countries


# In[8]:


dip["country"] = dip.location[dip.location.isin(known_countries)]


# In[9]:


dip["city"] = dip.location[dip.location.isin(known_cities)]


# In[10]:


# dip


# In[11]:


dip = dip.merge(worldCities, left_on='city', right_on='name', how='left')


# In[12]:


dip = dip.drop('name', axis=1)
dip = dip.drop('subcountry', axis=1)
dip = dip.drop('geonameid', axis=1)


# In[13]:


dip["country"] = dip.country_y.fillna(dip.country_x)
dip = dip.drop('country_y', axis=1)
dip = dip.drop('country_x', axis=1)


# In[14]:


# dip.head()


# In[15]:


countryCapitals = pd.read_csv("./country-capitals.csv")
# countryCapitals.head()


# In[16]:


dip = dip.merge(countryCapitals, how='left', left_on='country', right_on='CountryName')
dip = dip.drop("CountryName", axis=1)


# In[17]:


dip["city"] = dip.city.fillna(dip.CapitalName)
# dip


# In[18]:


def getTitle(careerPath):
    title = careerPath.iloc[0].fullName
    if not np.isnan(careerPath.iloc[0].yearOfBirth):
        if not np.isnan(careerPath.iloc[0].yearOfDeath):
            title += "({}-{})".format(int(careerPath.iloc[0].yearOfBirth), int(careerPath.iloc[0].yearOfDeath))
        else:
            title += "({}-)".format(int(careerPath.iloc[0].yearOfBirth))
    return "Foreign Postings – "+title


# In[19]:





def plot_career(careerPath):
    title = getTitle(careerPath)
    plt.figure(figsize=(120,60))

    m = Basemap(resolution='c', # c, l, i, h, f or None
                projection='cyl',
                fix_aspect=True)
    plt.title(title, fontsize=120)

    # m.drawmapboundary(fill_color='#46bcec')
    m.drawcoastlines()#color='#f2f2f2',lake_color='#46bcec')
    m.drawcountries(antialiased=False)
    long = 0
    lat = 51
    output = io.StringIO()
    
    for _, entry in careerPath.iterrows():
        if np.isnan(entry.CapitalLongitude) or np.isnan(entry.CapitalLatitude):
            continue
        if np.isnan(entry.yearPostingStart):
            print_statement = entry.country+"\n"
            
        elif np.isnan(entry.yearPostingEnd):
            print_statement = entry.country + "({}-)".format(int(entry.yearPostingStart))+"\n"
        else:
            print_statement = entry.country + "({}-{})".format(int(entry.yearPostingStart), int(entry.yearPostingEnd))+"\n"
#         print(print_statement)
        output.write(entry.job+"\n")
        output.write(print_statement)
        output.write("\n")
        m.drawgreatcircle(long,lat, entry.CapitalLongitude,entry.CapitalLatitude, del_s =1, lw=20)
        long, lat = entry.CapitalLongitude,entry.CapitalLatitude
    plt.text(x=-170, y=-80, s= output.getvalue(), fontsize=120)
    print(output.getvalue())
    plt.savefig("paths/"+title+".pdf")


# In[ ]:


if __name__ == "__main__":
    lastName = sys.argv[1]
    print(lastName)
    careerPath = dip[dip.lastName == lastName]
    all_matching_names = np.unique(careerPath.fullName.tolist())
    if len(all_matching_names) != 1:
        print("There are several diplomats with that name, please choose:")
        for i, entry in enumerate(all_matching_names):
            print("{}) {}".format(i+1, entry))
        entry_number = input("Which entry do you want (enter a number)?\n")
        if entry_number.isdigit():
            entry_number = int(entry_number) - 1
            if entry_number < 0 or entry_number >= len(all_matching_names):
                print("invalid entry")
            else:
                full_name =all_matching_names[entry_number]
                careerPath = dip[dip.fullName == full_name]
                plot_career(careerPath)
    else:
        plot_career(careerPath)


# In[20]:




# careerPath = dip[dip.fullName == "YOUNG, WILLIAM H., C.M.G."]
# plot_career(careerPath)

