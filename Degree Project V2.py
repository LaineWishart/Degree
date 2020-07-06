#!/usr/bin/env python
# coding: utf-8

# In[2]:


import requests
from bs4 import BeautifulSoup
import re 
import pandas as pd
import numpy as np


# In[7]:


url = 'https://www.sydney.edu.au/handbooks/science/subject_areas_ae/data_science_table.shtml'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html5lib')


# In[5]:


# get strings next to br_tags

def get_br_string(elements):
     brs = elements.find_all('br') # all descriptions next to br tag
     descr = []
     for br in brs:
        descr.append(br.previous_element)
     return descr


unitcodes = []
unit_descriptions = []
credit_points = []
semester = []
requirements = []


for tag in soup.find_all('tr'):
    
    if tag.td != None:
        if tag.strong != None:
            unitcode = tag.strong.next_element
            if unitcode != None:
                unit_descr = unitcode.next.next 
                # exclude units that don't have a unit description 
                if str(type(unit_descr)) != "<class 'bs4.element.NavigableString'>":
                    continue
                
                else:
                   
                    elements = unitcode.find_all_next("td")

                    # get credit_points 
                    cp_tags = elements[0]
                    cp = cp_tags.text

                    # get semester
                    sem_tags = elements[2]
                    sem = get_br_string(sem_tags)


                    # get requirements for each unit
                    reqs_and_tags = elements[1]
                    strong_tags  = reqs_and_tags.find_all('strong') # contained within strong tags
                    reqs = []

                    for tag in strong_tags:
                        reqs.append(tag.next_element.strip())

                    ## get descriptions of each requirement 
                    reqs_descr = get_br_string(reqs_and_tags)


                    ## create a dictionary holding requirements and their descriptions 
                    unit_requirements = {}
                    for i,j in zip(reqs, reqs_descr):
                       unit_requirements[i] = j

                    unitcodes.append(unitcode)
                    unit_descriptions.append(unit_descr)
                    credit_points.append(cp)
                    semester.append(sem)
                    requirements.append(unit_requirements)


# In[6]:


data = {'unitcode': unitcodes, 'unit_description': unit_descriptions, 'credit_points': credit_points, 
    'semester': semester, 'requirements': requirements}

data

df = pd.DataFrame(data, columns = ['unitcode', 'unit_description', 'credit_points', 'semester', 'requirements'])

df


# In[8]:





# In[12]:




