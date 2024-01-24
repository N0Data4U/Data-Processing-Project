# This file contains all necessary functions for scraping mobile phone data from the three used data sources: DatArt, CZC and Electroworld

# Loading packages
import requests, re;
from bs4 import BeautifulSoup;

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

    # Print the number of products found
    print(f"{len(product_urls)} products found.")
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
    # Print the number of products found
    print(f"{len(product_urls)} products found.")
    return product_urls

# 1.3 Electroworld - Function for sraping all product URLs of mobile phones from the mobile phone category page
def get_product_urls_electroworld(basic_url, category_urls,):
    
    # Check data types of arguments
    if not isinstance(basic_url, str):
        raise TypeError("Basic URL must be a string.")
    
    if not isinstance(category_urls, list):
        raise TypeError("Category URLs must be a list.")
    
    product_urls = []

    # Scrape product URL's across all product pages
    for page_num, url in enumerate(category_urls, start=1):

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
    # Print the number of products found
    print(f"{len(product_urls)} products found.")
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

# Function to return the rating for a given product (page) as a float number
def get_product_rating_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select('.rating-wrap')[0]:
        soup_ratings = soup_product_page.select('.rating-wrap')[0].text.replace('\n', '').replace('\t', '').strip().replace(" ", "")
        try:
            rating = float(re.match(r'(\d+\.\d+)\((\d+)\)', soup_ratings).group(1))
        except Exception:
            rating = float(re.match(r'(\d+)\((\d+)\)', soup_ratings).group(1))
    else: 
        rating = None
    return rating

# Function to return the number of ratings for a given product (page) as an integer
def get_product_no_ratings_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select('.rating-wrap')[0]:
        soup_ratings = soup_product_page.select('.rating-wrap')[0].text.replace('\n', '').replace('\t', '').strip().replace(" ", "")
        try:
            no_rating = int(re.match(r'(\d+\.\d+)\((\d+)\)', soup_ratings).group(2))
        except Exception:
            no_rating = int(re.match(r'(\d+)\((\d+)\)', soup_ratings).group(2))
    else: 
        no_rating = None
    return no_rating

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
        display_resolution = int(re.search(r'(\d+) × (\d+)', soup_display_resolution).group(1))
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
        display_resolution = int(re.search(r'(\d+) × (\d+)', soup_display_resolution).group(2))
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
        display_resolution = re.search(r'(\d+) × (\d+)', soup_display_resolution)
        display_resolution = int(display_resolution.group(1))*int(display_resolution.group(2))
    else:
        display_resolution = None
    # Return total display resolution as product of resolution in width and height
    return display_resolution

# Function to return the display refresh rate (in Hertz) for a given product (page) as an integer
def get_product_display_refresh_rate_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select_one('.table-borderless tbody th:contains("Obnovovací frekvence displeje") + td'):
        soup_display_refresh_rate = soup_product_page.select_one('.table-borderless tbody th:contains("Obnovovací frekvence displeje") + td').get_text()
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
        if cutout_shape not in ["drop", "bullet hole", "without cut-out"]:
            cutout_shape = "Other cutout-shape"
    else:
        cutout_shape = None
    return cutout_shape

# Function to return the processor manufacturer for a given product (page) as a string
def get_product_processor_manufacturer_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Výrobce procesoru") + td'):
        processor_manufacturer = str(soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Výrobce procesoru") + td').get_text())
    else:
        processor_manufacturer = None
    return processor_manufacturer

# Function to return the processor model for a given product (page) as a string
def get_product_processor_model_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Model procesoru") + td'):
        processor_model = str(soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Model procesoru") + td').get_text())
    else: processor_model = None
    return processor_model

# Function to return the number of cores for a given product (page) as a string
def get_product_no_cores_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Počet jader") + td'):
        no_cores = no_cores = str(soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Počet jader") + td').get_text())
        # Changing czech to english labelling. If there would be a new label, "Other core" will be printed.
        if no_cores == "osmijádrový":
            no_cores = "Octa-core"
        if no_cores == "šestijádrový":
            no_cores = "Hexa-core"
        if no_cores == "čtyřjádrový":
            no_cores = "Quad-Core"
        if no_cores not in ["Octa-core", "Hexa-core", "Quad-Core"]:
            no_cores = "Other core"
    else: 
        no_cores = None
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
    else:
        sim_card_type = None
    return sim_card_type

# Function to return the degree of protection for a given product (page) as a string
def get_product_degree_of_protection_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Stupeň krytí") + td'):
        degree_of_protection = str(soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Stupeň krytí") + td').get_text())
    else: 
        degree_of_protection = None
    return degree_of_protection#

# Function to return the operating system for a given product (page) as a string
def get_product_OS_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Operační systém") + td'):
        product_OS = str(soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Operační systém") + td').get_text())
    else: 
        product_OS = None
    return product_OS

# Function to return the system superstructure for a given product (page) as a string
def get_product_system_superstructure_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Nadstavba systému") + td'):
        system_superstructure = str(soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Nadstavba systému") + td').get_text())
    else: 
        system_superstructure = None
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
        notification_diode = None
    return notification_diode

# Function to return the internal memory (in GB) for a given product (page) as an integer
def get_product_int_memory_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Interní paměť") + td'):
        soup_internal_memory = soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Interní paměť") + td').get_text()
        internal_memory = int(re.search(r'(\d+)', soup_internal_memory).group(1))
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

# Function to return the maximum memory card size (in TB) for a given product (page) as an integer
def get_product_max_memory_card_size_DatArt(soup_product_page):
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
                max_memory_card_size = "Doesn't support memory cards"
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
        no_rear_cam_lenses = None
    return no_rear_cam_lenses

# Function to return the rear camera resolution (in Megapixels) for a given product (page) as a float number
def get_product_rear_cam_resolution_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    # Taking of highest resolution of the rear lenses as a proxy for the resolution of the rear camera in general
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Rozlišení zadního fotoaparátu") + td'):
        soup_rear_cam_resolution = str(soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Rozlišení zadního fotoaparátu") + td').get_text())
        rear_cam_resolution =  max([float(match.group()) for match in re.finditer(r'\b\d+\b', soup_rear_cam_resolution)])
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
        if camera_feature_list and all(element not in camera_feature_list for element in ["wide angle lens", "night mode", "auto focus", "flash diode", "Bokeh effect", "optical zoom", "macro mode", "telephoto"]):
            camera_feature_list = "Other camera feature(s)"
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
        battery_type = None
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
        if battery_feature_list and all(element not in battery_feature_list for element in ["fast charging", "wireless charging", "removable battery", "reverse wireless charging"]):
            battery_feature_list = "Other battery feature(s)"
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
        if security_list and all(element not in security_list for element in ["body fingerprint reader", "in-display fingerprint reader", "face unlock"]):
            security_list = "Other security option(s)"
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
        connector = None
    return connector

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
        if colour == "stříbrná ":
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
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Šířka výrobku") + td'):
        soup_product_width = soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Šířka výrobku") + td').get_text()
        product_width = float(re.search(r'(\d+\.\d+)', soup_product_width).group(1))
    else:
        product_width = None
    return product_width

# Function to return the height (in cm) for a given product (page) as a float number
def get_product_height_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Výška výrobku") + td'):
        soup_product_height = soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Výška výrobku") + td').get_text()
        product_height = float(re.search(r'(\d+\.\d+)', soup_product_height).group(1))
    else:
        product_height = None
    return product_height

# Function to return the depth (in cm) for a given product (page) as a float number
def get_product_depth_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Hloubka výrobku") + td'):
        soup_product_depth = soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Hloubka výrobku") + td').get_text()
        product_depth = float(re.search(r'(\d+\.\d+)', soup_product_depth).group(1))
    else: 
        product_depth = None
    return product_depth

# Function to return the volume (in cubic cm) for a given product (page) as a float number
def get_product_volume_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Šířka výrobku") + td'):
        soup_product_width = soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Šířka výrobku") + td').get_text()
        product_width = float(re.search(r'(\d+\.\d+)', soup_product_width).group(1))
    else:
        product_width = None
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Hloubka výrobku") + td'):
        soup_product_depth = soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Hloubka výrobku") + td').get_text()
        product_depth = float(re.search(r'(\d+\.\d+)', soup_product_depth).group(1))
    else:
        product_depth = None
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Výška výrobku") + td'):
        soup_product_height = soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Výška výrobku") + td').get_text()
        product_height = float(re.search(r'(\d+\.\d+)', soup_product_height).group(1))
    else:
        product_height = None
    if product_width*product_depth*product_height:
        volume = product_width*product_depth*product_height
    else:
        volume = None
    return volume

# Function to return the weight (in kg) for a given product (page) as a float number
def get_product_weight_DatArt(soup_product_page):
     # Check type of argument
    if not isinstance(soup_product_page, BeautifulSoup):
        raise TypeError(f"Input must be a BeautifulSoup object. Your input has the type: {type(soup_product_page)}.")
    if soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Hmotnost výrobku") + td'):
        soup_product_weight = soup_product_page.select_one('.table-borderless tbody th:-soup-contains("Hmotnost výrobku") + td').get_text()
        product_weight = float(re.search(r'(\d+\.\d+)', soup_product_weight).group(1))
    else:
        product_weight = None
    return product_weight

# 3. Functions for scraping product information characteristics for a given product (URL) from Electroworld
# For some variables (product colour, number of cores) an if-/elif-else clause was built to translate the czech labels into english labels
