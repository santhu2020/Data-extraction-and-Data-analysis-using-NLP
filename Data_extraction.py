#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import os
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService

input_excel_path = "C:\\Users\\santh\\Documents\\Blackcoffer_data\\Blackcoffer_data\\Input.xlsx"

df = pd.read_excel(input_excel_path)

webdriver_path = "D:\DOWNLOADS\chromedriver-win64_105\chromedriver-win64\chromedriver.exe"

chrome_service = ChromeService(webdriver_path)
driver = webdriver.Chrome(service=chrome_service)

def extract_article_text(url):
    driver.get(url)
    driver.implicitly_wait(10) 
    content=driver.find_elements(By.XPATH, "/html/body")
    article_title = driver.title
    res_list = []
    for p in range(len(content)):
        res_list.append(content[p].text)

    return res_list[0],article_title

output_directory = "output_texts"
os.makedirs(output_directory, exist_ok=True)

for index, row in df.iterrows():
    url_id = int(row['URL_ID'])  
    url = row['URL']

    article_text,article_title = extract_article_text(url)

    output_file_path = os.path.join(output_directory, f"{url_id}.txt")
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(f"Title: {article_title}\n\n")
        file.write(article_text)
        
print("Extraction and saving completed.")


# In[ ]:




