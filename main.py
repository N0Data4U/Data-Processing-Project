# 0. Installing packages, loading packages & modules

# loading packages 
import csv;
import requests;
import json;
from bs4 import BeautifulSoup;
from datetime import datetime;
import os;
from selenium import webdriver;
from selenium.webdriver.common.by import By;
from selenium.webdriver.support.ui import WebDriverWait as WBW;
from selenium.webdriver.support import expected_conditions as EC;

# Loading module with scraping functions
from scraper import *;

# 1. Scraping URL's of phone products

# DatArt
# 1 Finding the basic URL that can be extended to obtain the links of certain products
DatArt_basic_url = "https://www.datart.cz"
# 2 Finding category website with all the products listed (here by manually setting the limit of products shown manually in the browser)
DataArt_category_url = "https://www.datart.cz/mobilni-telefony.html?limit=1100" 
product_urls_DatArt = get_product_urls_DatArt(DatArt_basic_url, DataArt_category_url)

# Electroworld
# 1 Finding the basic URL that can be extended to obtain the links of certain products
Electroworld_basic_url = "https://www.electroworld.cz"

# 2 Finding category page with all the products listed (here no manual limit for the number of products shown can be set)
Electroworld_category_url =  "https://www.electroworld.cz/chytre-mobily/sort-by_mostExpensive" # sorted by most expensive gives unique products for each page

product_urls_Electroworld = get_product_urls_Electroworld(Electroworld_basic_url, Electroworld_category_url, 45) # Currently (06.02.2024) there are 41 pages of products

# 2. Scraping product information

# DatArt
# For all products (product URL's) found, the product information is scraped. For every characteristic, a function is defined in scraper.py. 
# For some variables like wireless technologies, lists of characteristics are scraped. 
# For each of these characteristics a 1-values is assigned to show that these characteristic is available.
products_DatArt = get_product_info_DatArt(product_urls_DatArt[0:2])

# Post-processing Data. Adding zero values for binary variables with missing values. After that the variables data type is changed to boolean.

# Keys to ensure they exist in each dictionary with a default value of 0
keys_binary = ['without fingerprint reader', 'Bokeh effect', '4G/LTE', 'Galileo', 'Beidou', 'auto focus', 'thermal camera', 'GPS', 'body fingerprint reader', 'removable battery', 'infrared', 'fast charging', 'wide angle lens', 'Wi-Fi', 'memory card slot', 'macro mode', 'night mode', 'FM-radio', 'optical zoom', '5G', 'wireless charging', 'face unlock', '3.5mm jack', 'NFC', 'GLONASS', 'telephoto', 'A-GPS', 'reverse wireless charging', 'in-display fingerprint reader', 'Bluetooth', 'flash diode', 'hybrid zoom']

# Adding default value of 0 to binary keys and convert into boolean 
gen_boolean_variables_data(products_DatArt, keys_binary)

# For some products the product width and length was confused on the product page. Therefore, for products with length <8 cm, the length and the width are interchanged. 
# After a manual check, this boundary was the highest appropriate to include all products that have a small product length.
gen_appropriate_length_and_width_DatArt(products_DatArt)

# Generating a csv file.
# Specify the paths for CSV files
path_csv_file = 'product_table_DatArt.csv'

# Open the JSON file and load its content
with open('product_info_DatArt.json', 'r') as json_file:
    Products_Data_DatArt = json.load(json_file)
    
# Creating a csv file in the working directory
gen_csv_file_data(path_csv_file, Products_Data_DatArt)

# Electroworld
# For the products (product URL's) from Electroworld, only the BeatifulSoup object is not enough to scrape the product characteristics. 
# Here, a large part of the product characteristics is hidden behind a button. 
# Therefore, the selenium module is used to click on the button in the background and scrape the data from the resulting dynamic webpage.
products_Electroworld = get_product_info_Electroworld(product_urls_Electroworld[0:2])

# Post-Processing. Adding zeros to missing values of binary variables. After that, converting these into boolean data type.
keys_binary = ['face unlock', 'body fingerprint reader', 'in-display fingerprint reader']

# Adding default value of 0 to binary keys and convert into boolean 
gen_boolean_variables_data(products_Electroworld, keys_binary)

# For some products the product depth and length was confused on the product page. Therefore, for products with length <2 cm, the length and the depth are interchanged.
gen_appropriate_length_and_depth_Electroworld(products_Electroworld)

# In Electroworld's sorting of the products there may be ducplicates of certain phones. These will be deleted here
# Safety: First copying list of product dictionaries
unique_products_Electroworld = remove_duplicates_Electroworld(products_Electroworld)

# Generating a json file "product_info_Electroworld.json" containing the list of product dictionaries.
# convert to JSON object and safe as JSON file
with open('product_info_Electroworld.json', 'w') as file:

    json.dump(products_Electroworld, file)

# Generating a csv file.

# Specify the paths for CSV files
path_csv_file = 'product_table_electroworld.csv'

# Open the JSON file and load its content
with open('product_info_Electroworld.json', 'r') as json_file:
    Products_Data_Electroworld = json.load(json_file)
    
# Creating a csv file in the working directory
gen_csv_file_data(path_csv_file, Products_Data_Electroworld)

## 3. Merging and Integrating Data
with open('product_info_DatArt.json', 'r') as json_file:
    Merge_Products_Data_DatArt = json.load(json_file)

with open('product_info_Electroworld.json', 'r') as json_file:
    Merge_Products_Data_Electroworld = json.load(json_file)

# Get the common variables of two lists of product dictionaries (DatArt, Electroworld)
common_variables = get_common_variables(Merge_Products_Data_DatArt, Merge_Products_Data_Electroworld)

# Create a new list of dictionaries with only the specified variables from both data sources
complete_products_list = []
for product_dict in Merge_Products_Data_DatArt + Merge_Products_Data_Electroworld:
    complete_products_list.append(extract_variables_from_product_dict(product_dict, common_variables))

# Add unique 'ID' to each product dictionary
id_counter = 1
for product_dict in complete_products_list:
    product_dict['ID'] = id_counter
    id_counter += 1

# Generating a json file "product_info_complete.json" containing the list of product dictionaries.
# convert to JSON object and safe as JSON file
with open('product_info_complete.json', 'w') as file:
    json.dump(complete_products_list, file)

# Generating a csv file.
# Open the JSON file and load its content
with open('product_info_complete.json', 'r') as json_file:
    Products_Data_complete = json.load(json_file)
    
# Specify the paths for CSV files
csv_file_path = 'product_table_complete.csv'

# Creating a csv file in the working directory
gen_csv_file_data(csv_file_path, Products_Data_complete)