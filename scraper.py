# This file contains all necessary functions for scraping mobile phone data from the three used data sources: DatArt, CZC and Electroworld

# Loading packages
from logging import config
import os;
import requests, re;
from bs4 import BeautifulSoup;
from datetime import datetime;
from selenium import webdriver;
from selenium.webdriver.common.by import By;
from selenium.webdriver.support.ui import WebDriverWait as WBW;
from selenium.webdriver.support import expected_conditions as EC;
# 1. Functions for scraping product URL's from all three online retailers

# 1.1 DatArt - Function for sraping all product URLs of mobile phones from the mobile phone category page
def get_product_urls_DatArt(basic_url: str, category_url: str):

    # Check data types of arguments
    if not isinstance(basic_url, str):
        raise TypeError("Basic URL must be a string.")
    
    if not isinstance(category_url, str):
        raise TypeError("Category URL must be a string.")
    
    response = requests.get(category_url)

    # Check status code of the response
    if response.status_code == 200: # 200 -> possible to get data 
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract product URLs using appropriate selectors
        product_urls = [[basic_url + item.a.get('href')] for item in soup.select('.item-title')]
        # Flatten the list
        product_urls= [url for sublist in product_urls for url in sublist]
        
    else:
        print(f"Failed fetching. Response error - {response.status_code}: {response.reason}")
    # Saving current time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Print the number of products found with a current timestamp
    print(f"{len(product_urls)} products found.({current_time})")
    return product_urls


# 1.2 CZC - Function for sraping all product URLs of mobile phones from the mobile phone category page
def get_product_urls_CZC(basic_url: str, category_urls: list):
    
    # Check data types of arguments
    if not isinstance(basic_url, str):
        raise TypeError("Basic URL must be a string.")
    
    if not isinstance(category_urls, list):
        raise TypeError("Category URLs must be a list.")
    
    product_urls = []

    # Scrape product URL's across all product pages
    for page_num, url in enumerate(category_urls, start=1):

        response = requests.get(url)
        
        # Check status code of the response
        if response.status_code == 200: # 200 -> possible to get data 
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract product URLs using appropriate selectors
            product_urls.append([[basic_url + item.a.get('href')] for item in soup.select('.tile-title')])
            print(f"Page {page_num} complete")
            
        else:
            print("Failed fetching page {page_num}. Response error - {response.status_code}: {response.reason}")

    # Flatten the list
    product_urls = [url for page_list in product_urls for product_list in page_list for url in product_list]
    # Saving current time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Print the number of products found with a current timestamp
    print(f"{len(product_urls)} products found.({current_time})")
    return product_urls

# 1.3 Electroworld - Function for sraping all product URLs of mobile phones from the mobile phone category page
def get_product_urls_Electroworld(basic_url, category_url, number_of_pages):
    
    # Check data types of arguments
    if not isinstance(basic_url, str):
        raise TypeError("Basic URL must be a string.")
    
    if not isinstance(category_url, str):
        raise TypeError("Category URL must be a string.")

    if not isinstance(number_of_pages, int):
        raise TypeError("Number of pages must be of type integer.")
    
    # Instead all pages of the category url have to be individually scraped
    page_urls = [category_url] # category_url is added as it is the first page with products

    # Generating URL for all pages of the category website

    # Create list of pages 
    pages = list(range(2, number_of_pages, 1)) 

    # Iterate over the pages and construct URLs for every page of the category website
    for page in pages:
        url_with_page = f"{category_url}?page={page}"
        page_urls.append(url_with_page)

    # Placeholder for product URLS
    product_urls = []

    # Scrape product URL's across all product pages
    for page_num, url in enumerate(page_urls, start=1):

        response = requests.get(url)
        
        if response.status_code == 200: # 200 -> possible to get data 
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract product URLs using appropriate selectors
            product_urls.append([[basic_url + item.get('href')] for item in soup.select('.product-box__link')])
            print(f"Page {page_num} complete")
        else:
            print(f"Failed fetching page {page_num}. Response error - {response.status_code}: {response.reason}")
            return []
    
    # Flatten the list
    product_urls = [url for page_list in product_urls for product_list in page_list for url in product_list]
    # Saving current time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Print the number of products found with a current timestamp
    print(f"{len(product_urls)} products found.({current_time})")
    return product_urls

# 2. Functions for scraping product information characteristics for a given product (URL) from DatArt
# For some variables (product colour, number of cores) an if-/elif-else clause was built to translate the czech labels into english labels

# Function to return the title for a given product (page) as a string
def get_product_title_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select('.product-detail-title')[0]:
        product_title = str(soup_product_page.select('.product-detail-title')[0].text)
    else: 
        product_title = None               
    return product_title

# Function to return the price (in CZK) for a given product (page) as an integer
def get_product_price_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select('.actual')[0]:
        product_price = int(soup_product_page.select('.actual')[0].text.replace('\n', '').replace('\t', '').replace('\xa0', '').replace('Kč', '').strip())
    else:
        product_price = None
    return product_price

# Function to return the number of ratings for a given product (page) as an integer
def get_product_no_ratings_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select('.rating-wrap')[0]:
        soup_ratings = soup_product_page.select('.rating-wrap')[0].text.replace('\n', '').replace('\t', '').strip().replace(" ", "")
        if soup_ratings == "Bezhodnocení":
            no_rating = 0
        else:
            try:
                no_rating = int(re.match(r'(\d+\.\d+)\((\d+)\)', soup_ratings).group(2))
            except Exception:
                no_rating = int(re.match(r'(\d+)\((\d+)\)', soup_ratings).group(2))
    else: 
        no_rating = None
    return no_rating

# Function to return the rating for a given product (page) as a float number
def get_product_rating_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select('.rating-wrap')[0]:
        soup_ratings = soup_product_page.select('.rating-wrap')[0].text.replace('\n', '').replace('\t', '').strip().replace(" ", "")
        # Set rating to NA if there are no ratings
        if soup_ratings == "Bezhodnocení":
            rating = None
        else:
            try:
                rating = float(re.match(r'(\d+\.\d+)\((\d+)\)', soup_ratings).group(1))
            except Exception:
                rating = float(re.match(r'(\d+)\((\d+)\)', soup_ratings).group(1))
    else: 
        rating = None
    return rating


# Function to return the display size (in inches) for a given product (page) as a float number
def get_product_display_size_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Úhlopříčka displeje") + td'):
        display_size = float(soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Úhlopříčka displeje") + td').get_text(strip=True).replace(',', '.'))
    else: 
        display_size = None
    return display_size

# Function to return the display resolution (width in pixels) for a given product (page) as an integer
def get_product_resolution_w_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Rozlišení displeje") + td'):
        soup_display_resolution = soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Rozlišení displeje") + td').get_text()
        try:
            display_resolution = int(re.search(r'(\d+) × (\d+)', soup_display_resolution).group(1))
        except Exception:
            display_resolution = int(re.search(r'(\d+) x (\d+)', soup_display_resolution).group(1))
    else:
        display_resolution = None
    return display_resolution

# Function to return the display resolution (height in pixels) for a given product (page) as an integer
def get_product_resolution_h_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Rozlišení displeje") + td'):
        soup_display_resolution = soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Rozlišení displeje") + td').get_text()
        try:
            display_resolution = int(re.search(r'(\d+) × (\d+)', soup_display_resolution).group(2))
        except Exception:
            display_resolution = int(re.search(r'(\d+) x (\d+)', soup_display_resolution).group(2))
    else: 
        display_resolution = None
    return display_resolution

# Function to return the display resolution (product of width and height in pixels) for a given product (page) as an integer
def get_product_resolution_tot_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Rozlišení displeje") + td'):
        soup_display_resolution = soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Rozlišení displeje") + td').get_text()
        try:
            display_resolution_w = int(re.search(r'(\d+) × (\d+)', soup_display_resolution).group(1))
            display_resolution_h = int(re.search(r'(\d+) × (\d+)', soup_display_resolution).group(2))
        except Exception:
            display_resolution_w = int(re.search(r'(\d+) x (\d+)', soup_display_resolution).group(1))
            display_resolution_h = int(re.search(r'(\d+) x (\d+)', soup_display_resolution).group(2))
        display_resolution = display_resolution_w*display_resolution_h
    else:
        display_resolution = None
    # Return total display resolution as product of resolution in width and height
    return display_resolution

# Function to return the display refresh rate (in Hertz) for a given product (page) as an integer
def get_product_display_refresh_rate_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Obnovovací frekvence displeje") + td'):
        soup_display_refresh_rate = soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Obnovovací frekvence displeje") + td').get_text()
        display_refresh_rate = int(re.search(r'(\d+)', soup_display_refresh_rate).group(1))
    else: 
        display_refresh_rate = None
    return display_refresh_rate

# Function to return the cutout shape for a given product (page) as a string
def get_product_cutout_shape_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Tvar výřezu") + td'):
        cutout_shape = str(soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Tvar výřezu") + td').get_text())
    # Changing czech to english labelling. If there would be a new label, "Other cutout-shape" will be printed.
        if cutout_shape == "kapka":
            cutout_shape = "drop"
        if cutout_shape == "obdélník":
            cutout_shape = "rectangle"
        if cutout_shape == "průstřel":
            cutout_shape = "bullet hole"
        if cutout_shape == "bez výřezu":
            cutout_shape = "without cut-out"
        if cutout_shape not in ["drop", "rectangle", "bullet hole", "without cut-out"]:
            cutout_shape = "other"
    else:
        cutout_shape = "other"
    return cutout_shape

# Function to return the processor manufacturer for a given product (page) as a string
def get_product_processor_manufacturer_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Výrobce procesoru") + td'):
        processor_manufacturer = str(soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Výrobce procesoru") + td').get_text())
    else:
        processor_manufacturer = "other"
    return processor_manufacturer

# Function to return the processor model for a given product (page) as a string
def get_product_processor_model_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Model procesoru") + td'):
        processor_model = str(soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Model procesoru") + td').get_text())
    else: processor_model = "other"
    return processor_model

# Function to return the number of cores for a given product (page) as a string
def get_product_no_cores_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Počet jader") + td'):
        no_cores = no_cores = str(soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Počet jader") + td').get_text())
        # Changing czech to english labelling. If there would be a new label, "Other core" will be printed.
        if no_cores == "desetijádrový":
            no_cores = 10
        if no_cores == "osmijádrový":
            no_cores = 8
        if no_cores == "šestijádrový":
            no_cores = 6
        if no_cores == "čtyřjádrový":
            no_cores = 4
        if no_cores not in [10, 8, 6, 4]:
            no_cores = "other"
    else: 
        no_cores = 0
    return no_cores

# Function to return the processor frequency (in GHZ) for a given product (page) as a float number
def get_product_processor_freq_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Frekvence procesoru") + td'):
        soup_processor_frequency = soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Frekvence procesoru") + td').get_text()
        processor_frequency = float(re.search(r'\(([\d,]+) GHz\)', soup_processor_frequency).group(1).replace(",", "."))
    else: 
        processor_frequency = None
    return processor_frequency

# Function to return the SIM card type for a given product (page) as a string
def get_product_SIM_card_type_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Typ Sim karty") + td'):
        sim_card_type = str(soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Typ Sim karty") + td').get_text())
        if sim_card_type == "2× nano SIM, nebo 1× nano SIM + eSIM":
            sim_card_type = "nano SIM + eSIM"
        if sim_card_type == "mini SIM Standardní":
            sim_card_type = "mini SIM Standard"
    else:
        sim_card_type = "other"
    return sim_card_type

# Function to return the configuration cards for a given product (page) as a string
def get_product_config_cards_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Konfigurace karet") + td'):
        configuration_cards = str(soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Konfigurace karet") + td').get_text())
        if configuration_cards == "Dual SIM (2× SIM)":
            configuration_cards = "Dual SIM (2x SIM)"
        if configuration_cards == "Dual SIM (2× SIM), nebo Single SIM + eSIM":
            configuration_cards = "Dual SIM (2x SIM), or Single SIM + eSIM"
        if configuration_cards == "Dual SIM + paměťová karta (2× SIM + pam. karta)":
            configuration_cards = "Dual SIM + Memory Card (2x SIM + Memory Card)"
        if configuration_cards == "Hybridní slot (2× SIM, nebo 1× SIM + pam. karta)":
            configuration_cards = "Hybrid slot (2x SIM or 1x SIM + memory card)"
        if configuration_cards == "Hybridní slot + eSIM":
            configuration_cards = "Hybrid slot + eSIM"
        if configuration_cards == "Single SIM + paměťová karta":
            configuration_cards = "Single SIM + memory card"
        if configuration_cards == "Single SIM + eSIM + paměťová karta":
            configuration_cards = "Single SIM + eSIM + Memory Card"
        if configuration_cards == "Single SIM (1× SIM)":
            configuration_cards = "Single SIM (1x SIM)"
    else:
        configuration_cards = "other"
    return configuration_cards

# Function to return the degree of protection for a given product (page) as a string
def get_product_degree_of_protection_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Stupeň krytí") + td'):
        degree_of_protection = str(soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Stupeň krytí") + td').get_text())
        if degree_of_protection == "nemá":
            degree_of_protection = "No protection"
        if degree_of_protection == "IP65/68":
            degree_of_protection = "IP68"
    else: 
        degree_of_protection = "No protection"
    return degree_of_protection

# Function to return the operating system for a given product (page) as a string
def get_product_OS_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Operační systém") + td'):
        product_OS = str(soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Operační systém") + td').get_text())
        if product_OS == "bez operačního systému":
            product_OS = "Without operating system"
        if product_OS == "vlastní OS":
            product_OS = "Custom operating system"
    else: 
        product_OS = "other"
    return product_OS

# Function to return the system superstructure for a given product (page) as a string
def get_product_system_superstructure_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Nadstavba systému") + td'):
        system_superstructure = str(soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Nadstavba systému") + td').get_text())
        if system_superstructure == "bez nadstavby":
            system_superstructure = "without superstructure"
        if system_superstructure == "čistý Android":
            system_superstructure = "pure Android"
    else: 
        system_superstructure = "other"
    return system_superstructure

# Function to return if the product has a notification diode for a given product (page) as a 1/0 variable
def get_product_notification_diode_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Notifikační dioda") + td'):
        notification_diode = str(soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Notifikační dioda") + td').get_text())
        if notification_diode == "Ano":
            notification_diode = 1
        if notification_diode == "Ne":
            notification_diode = 0
    else: 
        notification_diode = 0
    return bool(notification_diode)

# Function to return the internal memory (in GB) for a given product (page) as an integer
def get_product_int_memory_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Interní paměť") + td'):
        soup_internal_memory = soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Interní paměť") + td').get_text()
        if re.search(r'(\d+)', soup_internal_memory):
            internal_memory = int(re.search(r'(\d+)', soup_internal_memory).group(1))
        else:
            internal_memory = None # In some rare cases the internal memory is "yes". 
    else:
        internal_memory = None
    return internal_memory

# Function to return the amount of RAM (in GB) for a given product (page) as an integer
def get_product_RAM_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Velikost paměti RAM") + td'):
        soup_ram = soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Velikost paměti RAM") + td').get_text()
        ram = int(re.search(r'(\d+)', soup_ram).group(1))
    else:
        ram = None
    return ram

# Function to return if the product has a memory card slot for a given product (page) as a 1/0 variable
def get_product_memory_card_slot_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Podporované paměťové karty / typ karty") + td'):
        mem_card_slot = str(soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Podporované paměťové karty / typ karty") + td').get_text())
        if mem_card_slot == "nepodporuje":
            mem_card_slot = 0
        else: 
            mem_card_slot = 1
    else: 
        mem_card_slot = 0
    return bool(mem_card_slot)

# Function to return the maximum memory card size (in TB) for a given product (page) as an integer
def get_product_maximum_memory_card_size_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Maximální velikost paměťové karty") + td'):
        soup_max_memory_card_size = soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Maximální velikost paměťové karty") + td').get_text()
        # If there is a number extract the number (string), it is extracted
        try:
            max_memory_card_size = int(re.search(r'(\d+)', soup_max_memory_card_size).group(1))
        except Exception:
            max_memory_card_size = str(soup_max_memory_card_size)
            if max_memory_card_size == "nepodporuje paměťové karty":
                max_memory_card_size = None
    else:
        max_memory_card_size = None
    return max_memory_card_size

# Function to return a list of wireless technologies for a given product (page) as a list of string objects
def get_product_wireless_tech_list_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Bezdrátové technologie") + td'):
        wireless_tech_list = str(soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Bezdrátové technologie") + td').get_text()).split(', ')
        if "Infraport" in wireless_tech_list:
            # Find index to replace
            index = wireless_tech_list.index("Infraport")
            # Replace values
            wireless_tech_list[index] = "infrared"
    else:
        wireless_tech_list = None
    return wireless_tech_list

# Function to return the number of rear lenses for a given product (page) as an integer
def get_product_no_rear_cam_lenses_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Počet objektivů zadního fotoaparátu") + td'):
        no_rear_cam_lenses = int(soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Počet objektivů zadního fotoaparátu") + td').get_text())
    else:
        no_rear_cam_lenses = 0
    return no_rear_cam_lenses

# Function to return the number of front lenses for a given product (page) as an integer
def get_product_no_front_cam_lenses_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Počet objektivů předního fotoaparátu") + td'):
        no_front_cam_lenses = int(soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Počet objektivů předního fotoaparátu") + td').get_text())
    else:
        no_front_cam_lenses = 0
    return no_front_cam_lenses

# Function to return the rear camera resolution (in Megapixels) for a given product (page) as a float number
def get_product_rear_cam_resolution_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    # Taking of highest resolution of the rear lenses as a proxy for the resolution of the rear camera in general
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Rozlišení zadního fotoaparátu") + td'):
        soup_rear_cam_resolution = str(soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Rozlišení zadního fotoaparátu") + td').get_text())
        if re.search(r'\b\d+\b', soup_rear_cam_resolution):
            rear_cam_resolution =  max([float(match.group()) for match in re.finditer(r'\b\d+\b', soup_rear_cam_resolution)])
        else: 
            rear_cam_resolution = None # Sometimes the rear camera solution is "Without Camera"
    else:
        rear_cam_resolution = None
    return rear_cam_resolution

# Function to return the front camera resolution (in Megapixels) for a given product (page) as a float number
def get_product_front_cam_resolution_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Rozlišení předního fotoaparátu") + td'):
        soup_front_cam_resolution = soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Rozlišení předního fotoaparátu") + td').get_text()
        front_cam_resolution = float(re.search(r'(\d+)', soup_front_cam_resolution).group(1))
    else:
        front_cam_resolution = None
    return front_cam_resolution

# Function to return a list of camera features for a given product (page) as an list of strings
def get_product_camera_features_DatArt(soup_product_page):
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Funkce fotoaparátu") + td'):
        camera_feature_list = str(soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Funkce fotoaparátu") + td').get_text()).split(', ')
        # Changing czech to english labelling. If there would be a new label, "Other battery (features)" will be printed.
        if "širokoúhlý objektiv" in camera_feature_list:
            # Find index to replace
            index = camera_feature_list.index("širokoúhlý objektiv")
            # Replace values
            camera_feature_list[index] = "wide angle lens"
        if "noční režim" in camera_feature_list:
            # Find index to replace
            index = camera_feature_list.index("noční režim")
            # Replace values
            camera_feature_list[index] = "night mode"
        if "automatické ostření" in camera_feature_list:
            # Find index to replace
            index = camera_feature_list.index("automatické ostření")
            # Replace values
            camera_feature_list[index] = "auto focus"
        if "přisvětlovací dioda" in camera_feature_list:
            # Find index to replace
            index = camera_feature_list.index("přisvětlovací dioda")
            # Replace values
            camera_feature_list[index] = "flash diode"  
        if "Bokeh efekt" in camera_feature_list:
            # Find index to replace
            index = camera_feature_list.index("Bokeh efekt")
            # Replace values
            camera_feature_list[index] = "Bokeh effect"
        if "optický zoom" in camera_feature_list:
            # Find index to replace
            index = camera_feature_list.index("optický zoom")
            # Replace values
            camera_feature_list[index] = "optical zoom"
        if "přisvětlovací dioda" in camera_feature_list:
            index = camera_feature_list.index("přisvětlovací dioda")
            # Replace values
            camera_feature_list[index] = "LED flash"
        if "macro režim" in camera_feature_list:
            # Find index to replace
            index = camera_feature_list.index("macro režim")
            # Replace values
            camera_feature_list[index] = "macro mode"
        if "teleobjektiv" in camera_feature_list:
            # Find index to replace
            index = camera_feature_list.index("teleobjektiv")
            # Replace values
            camera_feature_list[index] = "telephoto"  
        if "hybridní zoom" in camera_feature_list:
            # Find index to replace
            index = camera_feature_list.index("hybridní zoom")
            # Replace values
            camera_feature_list[index] = "hybrid zoom" 
        if "termokamera" in camera_feature_list:
            # Find index to replace
            index = camera_feature_list.index("termokamera")
            # Replace values
            camera_feature_list[index] = "thermal camera"   
        if camera_feature_list and all(element not in camera_feature_list for element in ["wide angle lens", "night mode", "auto focus", "flash diode", "LED flash", "Bokeh effect", "optical zoom", "macro mode", "telephoto", "hybrid zoom", "thermal camera"]):
            camera_feature_list = ["Other camera feature(s)"]
    else:
        camera_feature_list = None
    return camera_feature_list

# Function to return the battery type for a given product (page) as an integer
def get_product_battery_type_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Typ akumulátoru") + td'):
        battery_type = str(soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Typ akumulátoru") + td').get_text())
    else: 
        battery_type = "other"
    return battery_type

# Function to return the battery capacity (in mAh) for a given product (page) as an integer
def get_product_battery_capacity_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Kapacita akumulátoru") + td'):
        soup_battery_capacity = soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Kapacita akumulátoru") + td').get_text()
        battery_capacity = int(re.search(r'(\d+)', soup_battery_capacity).group(1))
    else:
        battery_capacity = None
    return battery_capacity

# Function to return a list of battery features for a given product (page) as an list of strings
def get_product_battery_features_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Vlastnosti baterie") + td'):
        battery_feature_list = str(soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Vlastnosti baterie") + td').get_text()).split(', ')
        # Changing czech to english labelling. If there would be a new label, "Other battery feature(s)" will be printed.
        if "rychlé nabíjení" in battery_feature_list:
            # Find index to replace
            index = battery_feature_list.index("rychlé nabíjení")
            # Replace values
            battery_feature_list[index] = "fast charging"
        if "bezdrátové nabíjení" in battery_feature_list:
            # Find index to replace
            index = battery_feature_list.index("bezdrátové nabíjení")
            # Replace values
            battery_feature_list[index] = "wireless charging"
        if "vyjímatelná baterie" in battery_feature_list:
            # Find index to replace
            index = battery_feature_list.index("vyjímatelná baterie")
            # Replace values
            battery_feature_list[index] = "removable battery"
        if "reverzní bezdrátové nabíjení" in battery_feature_list:
            # Find index to replace
            index = battery_feature_list.index("reverzní bezdrátové nabíjení")
            # Replace values
            battery_feature_list[index] = "reverse wireless charging"
        if "reverzní kabelové nabíjení" in battery_feature_list:
            index = battery_feature_list.index("reverzní kabelové nabíjení")
            # Replace values
            battery_feature_list[index] = "reverse wireless charging"
        if battery_feature_list and all(element not in battery_feature_list for element in ["fast charging", "wireless charging", "removable battery", "reverse wireless charging"]):
            battery_feature_list = ["Other battery feature(s)"]
    else:
        battery_feature_list = None
    return battery_feature_list

# Function to return the charging power (in Watt) for a given product (page) as an integer
def get_product_charging_power_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Výkon nabíjení") + td'):
        soup_charging_power = str(soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Výkon nabíjení") + td').get_text())
        charging_power = int(re.search(r'(\d+)', soup_charging_power).group(1))
    else:
        charging_power = None
    return charging_power

# Function to return the securing option for a given product (page) as a string
def get_product_security_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Zabezpečení") + td'):
        security_list = str(soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Zabezpečení") + td').get_text()).split(', ')
        # Changing czech to english labelling. If there would be a new label, "Other security option(s)" will be printed.
        if "čtečka otisku prstů na těle" in security_list:
            # Find index to replace
            index = security_list.index("čtečka otisku prstů na těle")
            # Replace values
            security_list[index] = "body fingerprint reader"
        if "čtečka otisku prstů v displeji" in security_list:
            # Find index to replace
            index = security_list.index("čtečka otisku prstů v displeji")
            # Replace values
            security_list[index] = "in-display fingerprint reader"
        if "odemykání obličejem" in security_list:
            # Find index to replace
            index = security_list.index("odemykání obličejem")
            # Replace values
            security_list[index] = "face unlock"
        if "bez čtečky otisku prstů" in security_list:
            index = security_list.index("bez čtečky otisku prstů")
            # Replace values
            security_list[index] = "without fingerprint reader"
        if security_list and all(element not in security_list for element in ["body fingerprint reader", "in-display fingerprint reader", "face unlock", "without fingerprint reader"]):
            security_list = ["Other security option(s)"]
    else:
        security_list = None
    return security_list

# Function to return the connector for a given product (page) as a string
def get_product_connector_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Konektor") + td'):
        connector = str(soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Konektor") + td').get_text())
    else:
        connector = "other"
    return connector


# Function to return if the product has a 3.5mm jack for a given product (page) as a 1/0 variable
def get_product_3_5mm_jack_DatArt(soup_product_page):
    # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Jack 3,5 mm") + td'):
        jack_35mm = str(soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Jack 3,5 mm") + td').get_text())
        if jack_35mm == "Ano":
            jack_35mm = 1
        if jack_35mm == "Ne":
            jack_35mm = 0
    else: 
        jack_35mm = 0
    return bool(jack_35mm)

# Function to return the warranty (in months) for a given product (page) as an integer
def get_product_warranty_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Záruka") + td'):
        soup_warranty = soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Záruka") + td').get_text()
        warranty = int(re.search(r'(\d+)', soup_warranty).group(1))
    else:
        warranty = None
    return warranty

# Function to return if the product has a fm radio for a given product (page) as a 1/0 variable
def get_product_fm_radio_DatArt(soup_product_page):
    # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("FM rádio") + td'):
        fm_radio = str(soup_product_page.select_one('.table-borderless tbody th:-soup-contains("FM rádio") + td').get_text())
        if fm_radio == "Ano":
            fm_radio = 1
        if fm_radio == "Ne":
            fm_radio = 0
    else: 
        fm_radio = 0
    return bool(fm_radio)

# Function to return the colour for a given product (page) as a string
def get_product_colour_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Barva telefonu") + td'):
        colour = str(soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Barva telefonu") + td').get_text())
        # Changing czech to english labelling. If there would be a new label, "Other colour" will be printed.
        if colour == "modrá":
            colour = "blue"
        if colour == "tyrkysová":
            colour = "turquoise"        
        if colour == "zelená":
            colour = "green"
        if colour == "černá":
            colour = "black"
        if colour == "titanium":
            colour = "titanium"
        if colour == "vínová":
            colour = "burgundy"
        if colour == "šedá":
            colour = "grey"
        if colour == "fialová":
            colour = "purple"
        if colour == "béžová":
            colour = "beige"
        if colour == "stříbrná":
            colour = "silver"
        if colour == "zlatá":
            colour = "gold"
        if colour == "krémová":
            colour = "cream"
        if colour == "bílá":
            colour = "white"
        if colour == "červená":
            colour = "red"
        if colour == "oranžová":
            colour = "orange"
        if colour == "žlutá":
            colour = "yellow"
        if colour == "růžová":
            colour = "pink"
        if colour not in ["blue", "turquoise", "green", "black",  "titanium", "burgundy",  "grey", "purple", "beige", "silver", "gold", "cream", "white", "red", "orange", "yellow", "pink"]:
            colour = "Other colour"
    else:
        colour = None
    return colour
    
# Function to return the brand for a given product (page) as a string
def get_product_brand_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Značky") + td'):
        brand = str(soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Značky") + td').get_text())
    else:
        brand = None
    return brand

# Function to return the width (in cm) for a given product (page) as a float number
def get_product_width_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    # Locating the table with product dimensions
    if soup_product_page.select_one('.table-borderless tr th:-soup-contains("Rozměry výrobku")'):
        if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Šířka výrobku") + td'):
            soup_product_width = soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Šířka výrobku") + td').get_text()
            product_width = float(re.search(r'(\d+\.\d+)', soup_product_width).group(1))
            # For some products the commata is shifted by one digit 
            if product_width > 20:
                product_width = product_width/10
        else:
            product_width = None
    else:
        product_width = None
    return product_width

# Function to return the height (in cm) for a given product (page) as a float number
def get_product_length_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    # Locating the table with product dimensions
    if soup_product_page.select_one('.table-borderless tr th:-soup-contains("Rozměry výrobku")'):
        if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Výška výrobku") + td'):
            soup_product_length = soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Výška výrobku") + td').get_text()
            product_length = float(re.search(r'(\d+\.\d+)', soup_product_length).group(1))
        else:
            product_length = None
    else:
        product_length = None
    return product_length

# Function to return the depth (in cm) for a given product (page) as a float number
def get_product_depth_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    # Locating the table with product dimensions
    if soup_product_page.select_one('.table-borderless tr th:-soup-contains("Rozměry výrobku")'):
        if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Hloubka výrobku") + td'):
            soup_product_depth = soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Hloubka výrobku") + td').get_text()
            product_depth = float(re.search(r'(\d+\.\d+)', soup_product_depth).group(1))
        else: 
            product_depth = None
    else: 
        product_depth = None
    return product_depth

# Function to return the volume (in cubic cm) for a given product (page) as a float number
def get_product_volume_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    # Locating the table with product dimensions
    if soup_product_page.select_one('.table-borderless tr th:-soup-contains("Rozměry výrobku")'):
        if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Šířka výrobku") + td'):
            soup_product_width = soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Šířka výrobku") + td').get_text()
            product_width = float(re.search(r'(\d+\.\d+)', soup_product_width).group(1))
        else:
            product_width = None
    else: 
        product_width = None
    # Locating the table with product dimensions
    if soup_product_page.select_one('.table-borderless tr th:-soup-contains("Rozměry výrobku")'):
        if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Hloubka výrobku") + td'):
            soup_product_depth = soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Hloubka výrobku") + td').get_text()
            product_depth = float(re.search(r'(\d+\.\d+)', soup_product_depth).group(1))
        else:
            product_depth = None
    else: 
        product_depth
    # Locating the table with product dimensions
    if soup_product_page.select_one('.table-borderless tr th:-soup-contains("Rozměry výrobku")'):
        if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Výška výrobku") + td'):
            soup_product_length = soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Výška výrobku") + td').get_text()
            product_length = float(re.search(r'(\d+\.\d+)', soup_product_length).group(1))
        else:
            product_length = None
    else: 
        product_length
    if product_width*product_depth*product_length:
        volume = product_width*product_depth*product_length
    else:
        volume = None
    return volume

# Function to return the weight (in g) for a given product (page) as a float number
def get_product_weight_DatArt(soup_product_page):
    # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    # Locating the table with product dimensions
    if soup_product_page.select_one('.table-borderless tr th:-soup-contains("Rozměry výrobku")'):
        if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Hmotnost výrobku") + td'):
            soup_product_weight = soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Hmotnost výrobku") + td').get_text()
            product_weight = float(re.search(r'(\d+\.\d+)', soup_product_weight).group(1))
            # Multiplication to get the weight in grams
            product_weight_g = product_weight*1000
        else:
            product_weight_g = None
    else: 
        product_weight_g = None
    return product_weight_g


# Function to scrape all product information characteristics (for all URLs) from DatArt
def get_product_info_DatArt(product_url_list):

    # Check type of argument
    if not isinstance(product_url_list, list):
        raise TypeError(f"Input must be a list. Your input has the type: {type(product_url_list)}.")

    products_Data =[]
    for product_number, product_url in enumerate(product_url_list, start = 1):

        # Getting BeautifulSoup object of product (URL)
        page = requests.get(product_url)
        soup = BeautifulSoup(page.text, 'html.parser')

        # Placeholder for product characteristics
        product_entry_DatArt = {} 
        product_entry_DatArt["ID"] = product_number
        product_entry_DatArt["online-retailer"] = "DatArt"
        product_entry_DatArt['title'] = get_product_title_DatArt(soup)
        product_entry_DatArt['price'] = get_product_price_DatArt(soup)
        product_entry_DatArt['rating'] = get_product_rating_DatArt(soup)
        product_entry_DatArt['number of ratings'] = get_product_no_ratings_DatArt(soup)
        product_entry_DatArt['display size'] = get_product_display_size_DatArt(soup)
        product_entry_DatArt['resolution width'] = get_product_resolution_w_DatArt(soup)
        product_entry_DatArt['resolution height'] = get_product_resolution_h_DatArt(soup)
        product_entry_DatArt['resolution total'] = get_product_resolution_tot_DatArt(soup)
        product_entry_DatArt['display refresh rate'] = get_product_display_refresh_rate_DatArt(soup)
        product_entry_DatArt['cutout shape'] = get_product_cutout_shape_DatArt(soup)
        product_entry_DatArt['processor manufacturer'] = get_product_processor_manufacturer_DatArt(soup)
        product_entry_DatArt['processor model'] = get_product_processor_model_DatArt(soup)
        product_entry_DatArt['number of cores'] = get_product_no_cores_DatArt(soup)
        product_entry_DatArt['processor frequency'] = get_product_processor_freq_DatArt(soup)
        product_entry_DatArt['SIM card type'] = get_product_SIM_card_type_DatArt(soup)
        product_entry_DatArt['configuration cards'] = get_product_config_cards_DatArt(soup)
        product_entry_DatArt['degree of protection'] = get_product_degree_of_protection_DatArt(soup)
        product_entry_DatArt['operating system'] = get_product_OS_DatArt(soup)
        product_entry_DatArt['system superstructure'] = get_product_system_superstructure_DatArt(soup)
        product_entry_DatArt['notification diode'] = get_product_notification_diode_DatArt(soup)
        product_entry_DatArt['internal memory'] = get_product_int_memory_DatArt(soup)
        product_entry_DatArt['RAM'] = get_product_RAM_DatArt(soup)
        product_entry_DatArt['memory card slot'] = get_product_memory_card_slot_DatArt(soup)
        product_entry_DatArt['maximum memory card size'] = get_product_maximum_memory_card_size_DatArt(soup)

        if get_product_wireless_tech_list_DatArt(soup):
            for obj in get_product_wireless_tech_list_DatArt(soup):
                product_entry_DatArt[obj] = 1

        product_entry_DatArt['number of rear camera lenses'] = get_product_no_rear_cam_lenses_DatArt(soup)
        product_entry_DatArt['number of front camera lenses'] = get_product_no_front_cam_lenses_DatArt(soup)
        product_entry_DatArt['rear cam resolution'] = get_product_rear_cam_resolution_DatArt(soup)
        product_entry_DatArt['front cam resolution'] = get_product_front_cam_resolution_DatArt(soup)

        if get_product_camera_features_DatArt(soup):
            for obj in get_product_camera_features_DatArt(soup):
                product_entry_DatArt[obj] = 1

        product_entry_DatArt['battery type'] = get_product_battery_type_DatArt(soup)
        product_entry_DatArt['battery capacity'] = get_product_battery_capacity_DatArt(soup)

        if get_product_battery_features_DatArt(soup):
            for obj in get_product_battery_features_DatArt(soup):
                product_entry_DatArt[obj] = 1

        product_entry_DatArt['charging power'] = get_product_charging_power_DatArt(soup)

        if get_product_security_DatArt(soup):
            for obj in get_product_security_DatArt(soup):
                product_entry_DatArt[obj] = 1
        
        product_entry_DatArt['connector'] = get_product_connector_DatArt(soup)
        product_entry_DatArt['3.5mm jack'] = get_product_3_5mm_jack_DatArt(soup)
        product_entry_DatArt['warranty'] = get_product_warranty_DatArt(soup)
        product_entry_DatArt['FM-radio'] = get_product_fm_radio_DatArt(soup)
        product_entry_DatArt['colour'] = get_product_colour_DatArt(soup)
        product_entry_DatArt['brand'] = get_product_brand_DatArt(soup)
        product_entry_DatArt['width'] = get_product_width_DatArt(soup)
        product_entry_DatArt['length'] = get_product_length_DatArt(soup)
        product_entry_DatArt['depth'] = get_product_depth_DatArt(soup)
        product_entry_DatArt['volume'] = get_product_volume_DatArt(soup)
        product_entry_DatArt['weight'] = get_product_weight_DatArt(soup)

        products_Data.append(product_entry_DatArt)
        print(f"Product {product_number} finished")
    return products_Data

# 3. Functions for scraping product information characteristics for a given product (URL) from Electroworld

# Function to find the location of the chrome webdriver in the system path
def find_chromedriver():
    # Get the system PATH
    system_path = os.environ.get('PATH')

    # Split the PATH into individual directories
    path_dirs = system_path.split(os.pathsep)

    # Search for chromedriver.exe in all subdirectories of each directory
    for path_dir in path_dirs:
        for root, dirs, files in os.walk(path_dir):
            if 'chromedriver.exe' in files:
                chromedriver_path = os.path.join(root, 'chromedriver.exe')
                return chromedriver_path

    # If chromedriver.exe is not found in any directory or subdirectory
    return None

# Function to get the BeautifulSoup object for a given Electroworld product page
def get_soup_Electroworld(product_url, max_retries = 10):
    # Check type of argument
    if not isinstance(product_url, str):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(product_url)}.")
    
    for attempt in range(max_retries):
        try:
            # Starting driver
            driver = webdriver.Chrome()
            driver.get(product_url)
            # Finding the buttons on the product page
            buttons = WBW(driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'btn.w-100.maw-345px.btn-secondary.btn-sm')))

            # Pushing the button for product parameters
            desired_text = "Zobrazit všechny parametry"
            for button in buttons:
                if button.text == desired_text:
                    # Scroll to the element
                    driver.execute_script("arguments[0].scrollIntoView(true);", button)
                    # Execute a JavaScript click on the element
                    driver.execute_script("arguments[0].click();", button)
                    # Break out of the loop once the button is found and clicked
                    break
            # Go to the product parameters on the page
            WBW(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="product-params"]/div/div/div[2]/div[1]/table/tbody/tr[1]/th')))
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            return soup
        except Exception as e:
            print(f"Attempt {attempt + 1} failed. Exception: {str(e)}")
        finally:
             driver.quit()
# If all attempts fail, raise an exception
    raise Exception("Failed to retrieve data after multiple attempts")



# For some variables (product colour, number of cores) an if-/elif-else clause was built to translate the czech labels into english labels

# Function to return the title for a given product (page) as a string
def get_product_title_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.section__heading'):
            title = str(soup.select_one('.section__heading').get_text().replace("\n", "").strip())
        else:
            title = None
        return title

# Function to return the price for a given product (page) as an integer
def get_product_price_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product__discount-price.product__discount-price--no-border strong'):
            price = int(soup.select_one('.product__discount-price.product__discount-price--no-border strong').get_text().replace('\xa0', '').replace('Kč', '').strip())
        else:
            price = None
        return price

# Function to return the RAM for a given product (page) as an integer
def get_product_RAM_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("Operační paměť RAM") + td'):
            soup_RAM= soup.select_one('.product-parameters tbody th:-soup-contains("Operační paměť RAM") + td').get_text()
            RAM = int(re.search(r'(\d+)', soup_RAM).group(1))
        else:
            RAM = None
        return RAM

# Function to return the colour for a given product (page) as a string
def get_product_colour_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("Barva") + td'):
            colour = str(soup.select_one('.product-parameters tbody th:-soup-contains("Barva") + td').get_text().replace("\n", "").strip())
            # Changing czech to english labelling. If there would be a new label, "Other colour" will be printed.
            if colour == "černá":
                colour = "black"
            if colour == "modrá":
                colour = "blue"
            if colour == "zelená":
                colour = "green"
            if colour == "šedá":
                colour = "grey" 
            if colour == "bílá":
                colour = "white" 
            if colour == "fialová":
                colour = "purple" 
            if colour == "stříbrná":
                colour = "silver" 
            if colour == "žlutá":
                colour = "yellow" 
            if colour == "oranžová":
                colour = "orange" 
            if colour == "červená":
                colour = "red" 
            if colour == "růžová":
                colour = "pink" 
            if colour == "mix barev":
                colour = "mix"  
            if colour == "krémová":
                colour = "cream"
            if colour == "zlatá":
                colour = "gold"
            if colour == "béžová":
                colour = "beige"
            if colour == "tyrkysová":
                colour = "turquoise"
            if colour == "korálově červená":
                colour = "red" 
            if colour == "světle modrá":
                colour = "blue"
            if colour == "bronzová":
                colour = "bronze"
            if colour not in ["black", "blue", "green",  "grey", "white", "purple", "silver", "yellow", "orange", "red",  "pink", "mix",  "cream", "gold",  "beige", "turquoise", "bronze"]:
                colour = "Other colour"
        else:
            colour = None
        return colour

# Function to return the width (in cm) for a given product (page) as a float number
def get_product_width_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("Šířka") + td'):
            soup_product_width = soup.select_one('.product-parameters tbody th:-soup-contains("Šířka") + td').get_text()
            try: 
                product_width = (float(re.search(r'(\d+\.\d+)', soup_product_width).group(1)))/10
            except Exception:
                product_width = (float(re.search(r'(\d+)', soup_product_width).group(1)))/10
        else:
            product_width = None
        return product_width

# Function to return the depth (in cm) for a given product (page) as a float number
def get_product_depth_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("Výška") + td'):
            soup_product_depth = soup.select_one('.product-parameters tbody th:-soup-contains("Výška") + td').get_text()
            try:
                product_depth = (float(re.search(r'(\d+\.\d+)', soup_product_depth).group(1)))/10
            except Exception:
                product_depth = (float(re.search(r'(\d+)', soup_product_depth).group(1)))/10
        else:
            product_depth = None
        return product_depth

# Function to return the length (in cm) for a given product (page) as a float number
def get_product_length_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("Délka") + td'):
            soup_product_length = soup.select_one('.product-parameters tbody th:-soup-contains("Délka") + td').get_text()
            try:
                product_length = (float(re.search(r'(\d+\.\d+)', soup_product_length).group(1)))/10
            except Exception:
                product_length = (float(re.search(r'(\d+)', soup_product_length).group(1)))/10
        else:
            product_length = None
        return product_length

# Function to return the volume (in cubic cm) for a given product (page) as a float number
def get_product_volume_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("Šířka") + td'):
            soup_product_width = soup.select_one('.product-parameters tbody th:-soup-contains("Šířka") + td').get_text()
            try:
                product_width = (float(re.search(r'(\d+\.\d+)', soup_product_width).group(1)))/10
            except Exception:
                product_width = (float(re.search(r'(\d+)', soup_product_width).group(1)))/10
        else:
            product_width = None
        if soup.select_one('.product-parameters tbody th:-soup-contains("Výška") + td'):
            soup_product_depth = soup.select_one('.product-parameters tbody th:-soup-contains("Výška") + td').get_text()
            try:
                product_depth = (float(re.search(r'(\d+\.\d+)', soup_product_depth).group(1)))/10
            except Exception:
                product_depth = (float(re.search(r'(\d+)', soup_product_depth).group(1)))/10
        else:
            product_depth = None
        if soup.select_one('.product-parameters tbody th:-soup-contains("Délka") + td'):
            soup_product_length = soup.select_one('.product-parameters tbody th:-soup-contains("Délka") + td').get_text()
            try:
                product_length = (float(re.search(r'(\d+\.\d+)', soup_product_length).group(1)))/10
            except Exception:
                product_length = (float(re.search(r'(\d+)', soup_product_length).group(1)))/10
        else:
            product_length = None
        if product_width*product_depth*product_length:
            volume = product_width*product_depth*product_length
        else:
            volume = None
        return volume

# Function to return the weight (in grams) for a given product (page) as a float number
def get_product_weight_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("Hmotnost") + td'):
            soup_product_weight = soup.select_one('.product-parameters tbody th:-soup-contains("Hmotnost") + td').get_text()
            product_weight = float(re.search(r'(\d+)', soup_product_weight).group(1))
        else:
            product_weight = None
        return product_weight

# Function to return the bluetooth version for a given product (page) as a string
def get_product_bluetooth_version_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("Verze Bluetooth") + td'):
            bluetooth_version = str(soup.select_one('.product-parameters tbody th:-soup-contains("Verze Bluetooth") + td').get_text().replace("\n", "").strip())
        else:
            bluetooth_version = None
        return bluetooth_version

# Function to return 1 if a product has bluetooth, and 0 otherwise 
def get_product_bluetooth_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("Verze Bluetooth") + td'):
            bluetooth = 1
        else:
            bluetooth = 0
        return bool(bluetooth)

# Function to return the wifi standard for a given product (page) as a string
def get_product_wifi_standard_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("Wi-Fi standardy") + td'):
            wifi_standard = str(soup.select_one('.product-parameters tbody th:-soup-contains("Wi-Fi standardy") + td').get_text().replace("\n", "").strip())
            #Wi-Fi = 1
        else:
            wifi_standard = None
        return wifi_standard

# Function to return 1 if a product has wifi, and 0 otherwise 
def get_product_wifi_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("Wi-Fi standardy") + td'):
            wifi = 1
        else:
            wifi = 0
        return bool(wifi)

# Function to return 1 if a product has NFC, and 0 otherwise 
def get_product_NFC_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("NFC") + td'):
            NFC = str(soup.select_one('.product-parameters tbody th:-soup-contains("NFC") + td').get_text().replace("\n", "").strip())
            if NFC == "Ano":
                NFC = 1
            if NFC == "Ne":
                NFC = 0
        else:
            NFC = 0
        return bool(NFC)

# Function to return the connector for a given product (page) as a string
def get_product_connector_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("Konektor") + td'):
            connector = str(soup.select_one('.product-parameters tbody th:-soup-contains("Konektor") + td').get_text().replace("\n", "").strip())
        else:
            connector = "other"
        return connector

# Function to return 1 if a product has 3.5mm jack, and 0 otherwise 
def get_product_3_5_mm_jack_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("3,5 mm jack") + td'):
            jack = str(soup.select_one('.product-parameters tbody th:-soup-contains("3,5 mm jack") + td').get_text().replace("\n", "").strip())
            if jack == "Ano":
                 jack = 1
            if jack == "Ne":
                 jack = 0
        else:
            jack = 0
        return bool(jack)

# Function to return the display size (in cm) for a given product (page) as a float number
def get_product_display_size_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("Úhlopříčka") + td'):
            soup_display_size= soup.select_one('.product-parameters tbody th:-soup-contains("Úhlopříčka") + td').get_text()
            try:
                display_size = float(re.search(r'(\d+\.\d+)', soup_display_size).group(1))
            except Exception:
                display_size = float(re.search(r'(\d+)', soup_display_size).group(1))
        else:
            display_size = None
        return display_size

# Function to return the display type for a given product (page) as a string
def get_product_display_type_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("Typ displeje") + td'):
            display_type= str(soup.select_one('.product-parameters tbody th:-soup-contains("Typ displeje") + td').get_text().replace("\n", "").strip())
        else:
            display_type = None
        return display_type

# Function to return the display resolution width (in pixels) for a given product (page) as an integer
def get_product_display_resolution_w_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("Rozlišení displeje (px)") + td'):
            soup_display_resolution = soup.select_one('.product-parameters tbody th:-soup-contains("Rozlišení displeje (px)") + td').get_text().replace("\n", "").strip()
            display_resolution_w = int(re.search(r'(\d+)x(\d+)', soup_display_resolution).group(1))
        else:
            display_resolution_w = None
        return display_resolution_w

# Function to return the display resolution height (in pixels) for a given product (page) as an integer
def get_product_display_resolution_h_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("Rozlišení displeje (px)") + td'):
            soup_display_resolution = soup.select_one('.product-parameters tbody th:-soup-contains("Rozlišení displeje (px)") + td').get_text().replace("\n", "").strip()
            display_resolution_h = int(re.search(r'(\d+)x(\d+)', soup_display_resolution).group(2))
        else:
            display_resolution_h = None
        return display_resolution_h

# Function to return the display resolution in total (in pixels) for a given product (page) as an integer
def get_product_display_resolution_tot_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("Rozlišení displeje (px)") + td'):
            soup_display_resolution = soup.select_one('.product-parameters tbody th:-soup-contains("Rozlišení displeje (px)") + td').get_text().replace("\n", "").strip()
            display_resolution = re.search(r'(\d+)x(\d+)', soup_display_resolution)
            display_resolution = int(display_resolution.group(1))*int(display_resolution.group(2))
        else:
            display_resolution = None
        # Return total display resolution as product of resolution in width and height
        return display_resolution

# Function to return the display refresh rate (in Hertz) for a given product (page) as an integer
def get_product_display_refresh_rate_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("Obnovovací frekvence displeje") + td'):
            soup_display_refresh_rate = soup.select_one('.product-parameters tbody th:-soup-contains("Obnovovací frekvence displeje") + td').get_text().replace("\n", "").strip()
            display_refresh_rate = int(re.search(r'(\d+)', soup_display_refresh_rate).group(1))
        else:
            display_refresh_rate = None
        return display_refresh_rate

# Function to return the display resolution label for a given product (page) as a string
def get_product_display_resolution_label_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("Rozlišení displeje") + td'):
            display_resolution_label = soup.select_one('.product-parameters tbody th:-soup-contains("Rozlišení displeje") + td').get_text().replace("\n", "").strip()
        else:
            display_resolution_label = None
        return display_resolution_label

# Function to return the display fineness (in PPI) for a given product (page) as an integer
def get_product_display_fineness_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("Jemnost displeje (PPI)") + td'):
            soup_display_fineness = soup.select_one('.product-parameters tbody th:-soup-contains("Jemnost displeje (PPI)") + td').get_text().replace("\n", "").strip()
            display_fineness = int(re.search(r'(\d+)', soup_display_fineness).group(1))
        else:
            display_fineness = None
        return display_fineness

# Function to return the brand for a given product (page) as a string
def get_product_brand_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("Značka") + td'):
            brand = soup.select_one('.product-parameters tbody th:-soup-contains("Značka") + td').get_text().replace("\n", "").strip()
        else:
            brand = None
        return brand

# Function to return 1 if a product is "smart", and 0 otherwise 
def get_product_smart_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("Smart") + td'):
            smart = str(soup.select_one('.product-parameters tbody th:-soup-contains("Smart") + td').get_text().replace("\n", "").strip())
            if smart == "Ano":
                smart = 1
            if smart == "Ne":
                smart = 0
        else:
            smart = 0
        return bool(smart)

# Function to return 1 if a product is water-resistant, and 0 otherwise 
def get_product_water_resistant_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("Voděodolný") + td'):
            water_resistant = str(soup.select_one('.product-parameters tbody th:-soup-contains("Voděodolný") + td').get_text().replace("\n", "").strip())
            if water_resistant == "Ano":
                water_resistant = 1
            if water_resistant == "Ne":
                water_resistant = 0
        else:
            water_resistant = 0
        return bool(water_resistant)

# Function to return the degree of protection for a given product (page) as a string
def get_product_degree_of_protection_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("Stupeň krytí") + td'):
            degree_of_protection = str(soup.select_one('.product-parameters tbody th:-soup-contains("Stupeň krytí") + td').get_text().replace("\n", "").strip())
            if degree_of_protection == "nemá":
                degree_of_protection = "No protection"
        else:
            degree_of_protection = "No protection"
        return degree_of_protection

# Function to return the operating system for a given product (page) as a string
def get_product_operating_system_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("Verze operač.sys.") + td'):
            operating_system = str(soup.select_one('.product-parameters tbody th:-soup-contains("Verze operač.sys.") + td').get_text().replace("\n", "").strip())
            
        else:
            operating_system = "other"
        return operating_system

# Function to return the brand of the operating system for a given product (page) as a string
def get_product_os_brand_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("Poskytovaný OS") + td'):
            os_brand = str(soup.select_one('.product-parameters tbody th:-soup-contains("Poskytovaný OS") + td').get_text().replace("\n", "").strip())
            
        else:
            os_brand = None
        return os_brand

# Function to return 1 if a product has GPS, and 0 otherwise 
def get_product_gps_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("GPS") + td'):
            gps = str(soup.select_one('.product-parameters tbody th:-soup-contains("GPS") + td').get_text().replace("\n", "").strip())
            if gps == "Ano":
                gps = 1
            if gps == "Ne":
                gps = 0
        else:
            gps = 0
        return bool(gps)

# Function to return 1 if a product supports wireless charging, and 0 otherwise 
def get_product_wireless_charging_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("Bezdrátové nabíjení") + td'):
            wireless_charging = str(soup.select_one('.product-parameters tbody th:-soup-contains("Bezdrátové nabíjení") + td').get_text().replace("\n", "").strip())
            if wireless_charging  == "Ano":
                wireless_charging  = 1
            if wireless_charging  == "Ne":
                wireless_charging  = 0
        else:
            wireless_charging  = 0
        return bool(wireless_charging)

# Function to return 1 if a product contains fast charging, and 0 otherwise 
def get_product_fast_charging_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("Podpora rychlého nabíjení") + td'):
            fast_charging = str(soup.select_one('.product-parameters tbody th:-soup-contains("Podpora rychlého nabíjení") + td').get_text().replace("\n", "").strip())
            if fast_charging  == "Ano":
                fast_charging  = 1
            if fast_charging  == "Ne":
                fast_charging  = 0
        else:
            fast_charging  = 0
        return bool(fast_charging)

# Function to return a list of strings of security controls for a given product (page)
def get_product_security_controls_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("Prvky zabezpečení") + td'):
            security_controls = str(soup.select_one('.product-parameters tbody th:-soup-contains("Prvky zabezpečení") + td').get_text().replace("\n", "").strip()).split(', ')
            # Changing czech to english labelling. If there would be a new label, "Other security option(s)" will be printed.
            if "Odemykání tváří" in security_controls:
                # Find index to replace
                index = security_controls.index("Odemykání tváří")
                # Replace values
                security_controls[index] = "face unlock"
            if "Čtečka otisků prstů na těle" in security_controls:
                # Find index to replace
                index = security_controls.index("Čtečka otisků prstů na těle")
                # Replace values
                security_controls[index] = "body fingerprint reader"
            if "Čtečka otisků prstů v displeji" in security_controls:
                # Find index to replace
                index = security_controls.index("Čtečka otisků prstů v displeji")
                # Replace values
                security_controls[index] = "in-display fingerprint reader"
            if security_controls and all(element not in security_controls for element in ["face unlock", "body fingerprint reader", "in-display fingerprint reader"]):
                security_controls = ["Other security option(s)"]
        else:
            security_controls  = None
        return security_controls

# Function to return the manufacturer of the processor for a given product (page) as a string
def get_product_processor_manufacturer_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("Typ procesoru") + td'):
            processor_manufacturer = str(soup.select_one('.product-parameters tbody th:-soup-contains("Typ procesoru") + td').get_text().replace("\n", "").strip())
        else:
            processor_manufacturer  = "other"
        return processor_manufacturer

# Function to return the processor model for a given product (page) as a string
def get_product_processor_model_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("Verze procesoru") + td'):
            processor_model = str(soup.select_one('.product-parameters tbody th:-soup-contains("Verze procesoru") + td').get_text().replace("\n", "").strip())
        else:
            processor_model  = "other"
        return processor_model

# Function to return the number of cores for a given product (page) as an integer
def get_product_number_of_cores_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("Počet jader procesoru") + td'):
            number_of_cores = int(soup.select_one('.product-parameters tbody th:-soup-contains("Počet jader procesoru") + td').get_text().replace("\n", "").strip())
        else:
            number_of_cores  = 0
        return number_of_cores

# Function to return 1 if a product supports 4G/LTE, and 0 otherwise 
def get_product_4G_LTE_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("4G / LTE") + td'):
            LTE_4G = str(soup.select_one('.product-parameters tbody th:-soup-contains("4G / LTE") + td').get_text().replace("\n", "").strip())
            if LTE_4G  == "Ano":
                LTE_4G  = 1
            if LTE_4G  == "Ne":
                LTE_4G  = 0
        else:
            LTE_4G  = 0
        return bool(LTE_4G)

# Function to return 1 if a product contains dual SIM, and 0 otherwise 
def get_product_dual_sim_support_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("Podpora Dual SIM") + td'):
            dual_sim_support = str(soup.select_one('.product-parameters tbody th:-soup-contains("Podpora Dual SIM") + td').get_text().replace("\n", "").strip())
            if dual_sim_support  == "Ano":
                dual_sim_support  = 1
            if dual_sim_support  == "Ne":
                dual_sim_support  = 0
        else:
            dual_sim_support  = 0
        return bool(dual_sim_support)

# Function to return the sim card type for a given product (page) as a string
def get_product_sim_card_type_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("Typ SIM karty") + td'):
            sim_card_type = str(soup.select_one('.product-parameters tbody th:-soup-contains("Typ SIM karty") + td').get_text().replace("\n", "").strip())
            if sim_card_type == "nano sim":
                sim_card_type = "nano SIM"
            if sim_card_type == "eSIM, nano sim":
                sim_card_type = "nano SIM + eSIM"
        else:
            sim_card_type  = "other"
        return sim_card_type

# Function to return 1 if a product supports 5G, and 0 otherwise 
def get_product_5G_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("5G") + td'):
            dummy_5G = str(soup.select_one('.product-parameters tbody th:-soup-contains("5G") + td').get_text().replace("\n", "").strip())
            if dummy_5G  == "Ano":
                dummy_5G  = 1
            if dummy_5G  == "Ne":
                dummy_5G  = 0
        else:
            dummy_5G  = 0
        return bool(dummy_5G)

# Function to return the configuration cards for a given product (page) as a string
def get_product_config_cards_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("Konfigurace karet") + td'):
            config_cards = str(soup.select_one('.product-parameters tbody th:-soup-contains("Konfigurace karet") + td').get_text().replace("\n", "").strip())
            if config_cards == "Dual SIM + paměťová karta":
                config_cards = "Dual SIM + memory card"
            if config_cards == "Dual SIM, Single SIM + paměťová karta":
                config_cards = "Dual SIM, Single SIM + memory card"
            if config_cards == "Single SIM + paměťová karta":
                config_cards = "Single SIM + memory card"
            if config_cards == "Single SIM + eSIM + paměťová karta":
                config_cards = "Single SIM + eSIM + Memory Card"
            if config_cards == "Single SIM + paměťová karta, Dual SIM":
                config_cards = "Single SIM + Memory Card, Dual SIM"
            if config_cards == "Single SIM + paměťová karta, Single SIM + eSIM, eSIM + paměťová karta":
                config_cards = "Single SIM + Memory Card, Single SIM + eSIM, eSIM + Memory Card"
            if config_cards == "Single SIM + eSIM, Single SIM + paměťová karta, eSIM + paměťová karta":
                config_cards = "Single SIM + eSIM, Single SIM + Memory Card, eSIM + Memory Card"
            if config_cards == "Single SIM + eSIM, eSIM + paměťová karta, Single SIM + paměťová karta":
                config_cards = "Single SIM + eSIM, eSIM + Memory Card, Single SIM + Memory Card"
        else:
            config_cards  = "other"
        return config_cards

# Function to return 1 the product contains a memory card slot, and 0 otherwise 
def get_product_memory_card_slot_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("Slot pro paměťovou kartu") + td'):
            memory_card_slot = str(soup.select_one('.product-parameters tbody th:-soup-contains("Slot pro paměťovou kartu") + td').get_text().replace("\n", "").strip())
            if memory_card_slot == "Ano":
                 memory_card_slot = 1
            if memory_card_slot == "Ne":
                 memory_card_slot = 0
        else:
            memory_card_slot  = 0
        return bool(memory_card_slot)

# Function to return the battery capacity (in mAh) for a given product (page) as an integer
def get_product_battery_capacity_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("Kapacita batérie") + td'):
            soup_battery_capacity = soup.select_one('.product-parameters tbody th:-soup-contains("Kapacita batérie") + td').get_text()
            battery_capacity = int(re.search(r'(\d+)', soup_battery_capacity).group(1)) 
        else:
            battery_capacity  = None
        return battery_capacity

# Function to return the charging power/wireless charging power (in W) for a given product (page) as an integer
def get_product_charging_power_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("Výkon nabíjení") + td'):
            soup_charging_power = soup.select_one('.product-parameters tbody th:-soup-contains("Výkon nabíjení") + td').get_text()
            charging_power = int(re.search(r'(\d+)', soup_charging_power).group(1)) 
        else:
            charging_power  = None
        return charging_power

# Function to return the internal memory (in GB) for a given product (page) as an integer
def get_product_internal_memory_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("Kapacita") + td'):
            soup_internal_memory = soup.select_one('.product-parameters tbody th:-soup-contains("Kapacita") + td').get_text()
            internal_memory = int(re.search(r'(\d+)', soup_internal_memory).group(1)) 
        else:
            internal_memory  = None
        return internal_memory


# Function to return 1 the product contains a front camera, and 0 otherwise 
def get_product_front_cam_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("Přední fotoaparát") + td'):
            front_cam = str(soup.select_one('.product-parameters tbody th:-soup-contains("Přední fotoaparát") + td').get_text().replace("\n", "").strip())
            if front_cam == "Ano":
                front_cam  = 1
            if front_cam  == "Ne":
                front_cam  = 0
        else:
            front_cam  = 0
        return bool(front_cam)

# Function to return the rear camera resolutio (in pixels) for a given product (page) as a float number
def get_product_rear_cam_resolution_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("Rozlišení hl.fotoaparátu") + td'):
            soup_rear_cam_resolution = soup.select_one('.product-parameters tbody th:-soup-contains("Rozlišení hl.fotoaparátu") + td').get_text()
            rear_cam_resolution =  max([float(match.group()) for match in re.finditer(r'\b\d+\b', soup_rear_cam_resolution)])
        else:
            rear_cam_resolution  = None
        return rear_cam_resolution

# Function to return the front camera resolutio (in pixels) for a given product (page) as a float number
def get_product_front_cam_resolution_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("Rozlišení před.fotoaparátu") + td'):
            soup_front_cam_resolution = soup.select_one('.product-parameters tbody th:-soup-contains("Rozlišení před.fotoaparátu") + td').get_text()
            front_cam_resolution =  max([float(match.group()) for match in re.finditer(r'\b\d+\b', soup_front_cam_resolution)])
        else:
            front_cam_resolution  = None
        return front_cam_resolution

# Function to return the number of rear camera for a given product (page) as an integer
def get_product_no_rear_cam_lenses_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("Počet objektivů zadního fotoaparátu") + td'):
            no_rear_cam_lenses = int(soup.select_one('.product-parameters tbody th:-soup-contains("Počet objektivů zadního fotoaparátu") + td').get_text())
        else:
            no_rear_cam_lenses  = None
        return no_rear_cam_lenses

# Function to return the number of front camera for a given product (page) as an integer
def get_product_no_front_cam_lenses_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("Počet objektivů predního fotoaparátu") + td'):
            no_front_cam_lenses = int(soup.select_one('.product-parameters tbody th:-soup-contains("Počet objektivů predního fotoaparátu") + td').get_text())
        else:
            no_front_cam_lenses  = None
        return no_front_cam_lenses

# Function to return 1 the product contains a FM radio, and 0 otherwise 
def get_product_fm_radio_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("FM rádio") + td'):
            fm_radio = str(soup.select_one('.product-parameters tbody th:-soup-contains("FM rádio") + td').get_text().replace("\n", "").strip())
            if fm_radio == "Ano":
                fm_radio  = 1
            if fm_radio == "Ne":
                fm_radio  = 0
        else:
            fm_radio  = 0
        return bool(fm_radio)

# Function to return 1 the product contains a buil-in-flash, and 0 otherwise 
def get_product_built_in_flash_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("Přední fotoaparát") + td'):
            built_in_flash = str(soup.select_one('.product-parameters tbody th:-soup-contains("Přední fotoaparát") + td').get_text().replace("\n", "").strip())
            if built_in_flash == "Ano":
                built_in_flash  = 1
            if built_in_flash  == "Ne":
                built_in_flash  = 0
        else:
            built_in_flash  = 0
        return bool(built_in_flash)

# Function to return the flash type for a given product (page) as an string
def get_product_flash_type_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("Typ blesku") + td'):
            flash_type = str(soup.select_one('.product-parameters tbody th:-soup-contains("Typ blesku") + td').get_text().replace("\n", "").strip())
        else:
            flash_type  = None
        return flash_type

# Function to return the charging performance (in W) for a given product (page) as an integer
def get_product_wireless_charging_performance_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.product-parameters tbody th:-soup-contains("Výkon bezdrátového nabíjení") + td'):
            soup_wireless_charging_performance = soup.select_one('.product-parameters tbody th:-soup-contains("Výkon bezdrátového nabíjení") + td').get_text().replace("\n", "").strip()
            wireless_charging_performance = int(re.search(r'(\d+)', soup_wireless_charging_performance).group(1))
        else:
            wireless_charging_performance = 0
        return wireless_charging_performance

# Function to return the number of ratings for a given product (page) as an integer
def get_product_no_ratings_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.star-rating.mb-4.text-center.text-light.typo-complex-14'):
            soup_no_ratings = soup.select_one('.star-rating.mb-4.text-center.text-light.typo-complex-14').get_text().replace("\n", "").strip()
            no_ratings = int(re.search(r'\b\d+\b', soup_no_ratings).group(0))
        else:
            no_ratings = None
        return no_ratings

# Function to return the number of rating for a given product (page) as a float number
def get_product_rating_Electroworld(soup):
        # Check type of argument
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup)}.")
        if soup.select_one('.average-rating__average'):
            rating = float(soup.select_one('.average-rating__average').get_text().replace(",", "."))
            # Set rating to NA if there are no ratings
            if get_product_no_ratings_Electroworld(soup) == 0:
                rating = None
        else:
            rating = None
        return rating

# Function to scrape all product information characteristics (for all URLs) from Electroworld
def get_product_info_Electroworld(product_url_list):
    # Check type of argument
    if not isinstance(product_url_list, list):
        raise TypeError(f"Input must be a list. Your input has the type: {type(product_url_list)}.")
    # Placeholder list for product dictionaries
    products_Data =[]
    for product_number, product_url in enumerate(product_url_list, start = 1):
        # Placeholder dictionary for product characteristics
        product_entry_Electroworld = {} 
        # A large part of the product characteristics is hidden behind a button to extend the parameters shown on the product page
        # Here the selenium package is used to push the button of the webpage in the background to scrape the hidden product information
        try:
            soup = get_soup_Electroworld(product_url)
        except Exception as e:
            print(f"Failed to retrieve data. Final Exception: {str(e)}")
        product_entry_Electroworld["ID"] = product_number 
        product_entry_Electroworld["online-retailer"] = "Electroworld" 
        product_entry_Electroworld["title"] = get_product_title_Electroworld(soup) 
        product_entry_Electroworld["price"] = get_product_price_Electroworld(soup) 
        product_entry_Electroworld["colour"] = get_product_colour_Electroworld(soup) 
        product_entry_Electroworld["RAM"] = get_product_RAM_Electroworld(soup) 
        product_entry_Electroworld["width"] = get_product_width_Electroworld(soup) 
        product_entry_Electroworld["depth"] = get_product_depth_Electroworld(soup) 
        product_entry_Electroworld["length"] = get_product_length_Electroworld(soup) 
        product_entry_Electroworld["volume"] = get_product_volume_Electroworld(soup) 
        product_entry_Electroworld["weight"] = get_product_weight_Electroworld(soup) 
        product_entry_Electroworld["bluetooth version"] = get_product_bluetooth_version_Electroworld(soup) 
        product_entry_Electroworld["Bluetooth"] = get_product_bluetooth_Electroworld(soup) 
        product_entry_Electroworld["WiFi standard"] = get_product_wifi_standard_Electroworld(soup) 
        product_entry_Electroworld["Wi-Fi"] = get_product_wifi_Electroworld(soup) 
        product_entry_Electroworld["NFC"] = get_product_NFC_Electroworld(soup) 
        product_entry_Electroworld["connector"] = get_product_connector_Electroworld(soup) 
        product_entry_Electroworld["3.5mm jack"] = get_product_3_5_mm_jack_Electroworld(soup) 
        product_entry_Electroworld["display size"] = get_product_display_size_Electroworld(soup) 
        product_entry_Electroworld["display type"] = get_product_display_type_Electroworld(soup) 
        product_entry_Electroworld["resolution width"] = get_product_display_resolution_w_Electroworld(soup) 
        product_entry_Electroworld["resolution height"] = get_product_display_resolution_h_Electroworld(soup) 
        product_entry_Electroworld["resolution total"] = get_product_display_resolution_tot_Electroworld(soup) 
        product_entry_Electroworld["display refresh rate"] = get_product_display_refresh_rate_Electroworld(soup) 
        product_entry_Electroworld["resolution label"] = get_product_display_resolution_label_Electroworld(soup) 
        product_entry_Electroworld["display fineness"] = get_product_display_fineness_Electroworld(soup) 
        product_entry_Electroworld["brand"] = get_product_brand_Electroworld(soup) 
        product_entry_Electroworld["smart"] = get_product_smart_Electroworld(soup) 
        product_entry_Electroworld["water resistant"] = get_product_water_resistant_Electroworld(soup) 
        product_entry_Electroworld["degree of protection"] = get_product_degree_of_protection_Electroworld(soup)
        product_entry_Electroworld["operating system"] = get_product_operating_system_Electroworld(soup) 
        product_entry_Electroworld["os brand"] = get_product_os_brand_Electroworld(soup)
        product_entry_Electroworld["GPS"] = get_product_gps_Electroworld(soup) 
        product_entry_Electroworld["wireless charging"] = get_product_wireless_charging_Electroworld(soup) 
        product_entry_Electroworld["fast charging"] = get_product_fast_charging_Electroworld(soup) 
        if get_product_security_controls_Electroworld(soup): 
            for obj in get_product_security_controls_Electroworld(soup):
                product_entry_Electroworld[obj] = 1
        product_entry_Electroworld["processor manufacturer"] = get_product_processor_manufacturer_Electroworld(soup) 
        product_entry_Electroworld["processor model"] = get_product_processor_model_Electroworld(soup) 
        product_entry_Electroworld["number of cores"] = get_product_number_of_cores_Electroworld(soup) 
        product_entry_Electroworld["4G/LTE"] = get_product_4G_LTE_Electroworld(soup) 
        product_entry_Electroworld["dual SIM support"] = get_product_dual_sim_support_Electroworld(soup) 
        product_entry_Electroworld["SIM card type"] = get_product_sim_card_type_Electroworld(soup) 
        product_entry_Electroworld["5G"] = get_product_5G_Electroworld(soup) 
        product_entry_Electroworld["configuration cards"] = get_product_config_cards_Electroworld(soup)
        product_entry_Electroworld["memory card slot"] = get_product_memory_card_slot_Electroworld(soup) 
        product_entry_Electroworld["battery capacity"] = get_product_battery_capacity_Electroworld(soup) 
        product_entry_Electroworld["charging power"] = get_product_charging_power_Electroworld(soup) 
        product_entry_Electroworld["internal memory"] = get_product_internal_memory_Electroworld(soup) 
        product_entry_Electroworld["front cam"] = get_product_front_cam_Electroworld(soup) 
        product_entry_Electroworld["rear cam resolution"] = get_product_rear_cam_resolution_Electroworld(soup) 
        product_entry_Electroworld["front cam resolution"] = get_product_front_cam_resolution_Electroworld(soup) 
        product_entry_Electroworld["number of rear camera lenses"] =  get_product_no_rear_cam_lenses_Electroworld(soup) 
        product_entry_Electroworld["number of front camera lenses"] = get_product_no_front_cam_lenses_Electroworld(soup) 
        product_entry_Electroworld["FM-radio"] = get_product_fm_radio_Electroworld(soup) 
        product_entry_Electroworld["built-in flash"] = get_product_built_in_flash_Electroworld(soup) 
        product_entry_Electroworld["flash type"] = get_product_flash_type_Electroworld(soup) 
        product_entry_Electroworld["wireless charging performance"] = get_product_wireless_charging_performance_Electroworld(soup) 
        product_entry_Electroworld["number of ratings"] = get_product_no_ratings_Electroworld(soup) 
        product_entry_Electroworld["rating"] = get_product_rating_Electroworld(soup) 
        products_Data.append(product_entry_Electroworld)
        print(f"Product {product_number} finished")
    return products_Data

# 4. Functions for merging data from multiple lists of product dictionaries

# Function to get the common keys of two lists of dictionaries 
def get_common_variables(dataset_1, dataset_2):
    # Check type of arguments
    if not isinstance(dataset_1, list):
        raise TypeError(f"Input must be a list. Your input has the type: {type(dataset_1)}.")
    if not isinstance(dataset_2, list):
        raise TypeError(f"Input must be a list. Your input has the type: {type(dataset_2)}.")
    # Extracting the names of all variables from both data sets (DatArt and Electroworld). Thereby, excluding the ID variable.
    keys_dataset_1 = set().union(*(variable.keys() - {'ID'} for variable in dataset_1))
    keys_dataset_2 = set().union(*(variable.keys() - {'ID'} for variable in dataset_2))
    # Get the common variables
    return keys_dataset_1.intersection(keys_dataset_2)

# Function to extract relevant variables from a product dictionary
def extract_variables(product_dict, list_of_variables):
    # Check type of arguments
    if not isinstance(product_dict, dict):
        raise TypeError(f"Input must be a dictionary. Your input has the type: {type(product_dict)}.")
    if not isinstance(list_of_variables, set):
        raise TypeError(f"Input must be a set. Your input has the type: {type(list_of_variables)}.")
    return {variable: product_dict[variable] for variable in list_of_variables}