# Data-Processing-Project

This final project is part of the Data Processing in Python (JEM207) course at IES.
This project is about scraping, procesing and, analysis mobile phone data, utilizing the python programming language.
Precisely, we scrape data from three Czech online retailers using the BeautifulSoup library. During the data processing 
stage we try to transform data from multiple sources into a uniform format. Finally, multiple phone characteristics are 
used to draw coclusions about the phone prices.



<img width="1054" alt="Screenshot 2024-01-17 at 19 10 50" src="https://github.com/N0Data4U/Data-Processing-Project/assets/126565081/23ec8197-236d-4b82-b34d-1edf0e221eb3">

Next Steps:
1) Use of Git to do proper documenting and commiting of changes.
2) Finish the pipeline:
  2.1) Getting product informations
    2.1.1) (.) DatArt (getting also the age of the product as a variable)
    2.1.2) (.) CZC
    2.1.3) (.) Electroworld
  2.2) Integrate the information from three sources -> JSON/CSV files
  2.3) Summary statistics
  2.4) Visualizations
  2.5) Statistical Approach: Rather regression than PCA (https://shap.readthedocs.io/en/latest/example_notebooks/overviews/An%20introduction%20to%20explainable%20AI%20with%20Shapley%20values.html)
3) Proper functioning
   3.1) Creating one scraper.py file, including only functions (rather small functions, better for testing): e.g. get_sim_card_type()
   3.2) Testing functions -> testing inputs and outputs of the function. How to properly test the functions?
   3.3) Docstrings? Proper commenting of the code
4) Proper Packaging
     4.1) Requirements file
     4.2) Having proper modules in general
     4.3) Importing functions from scraper.py file (3.1) for usage
5) User Usability:
     5.1) Automatic Prediction: Provide information and get results for prices of a phone with certain characteristics
     5.2) Make it runnable 
  
### ChromeDriver Installation
1. Download the [ChromeDriver]([https://sites.google.com/chromium.org/driver/](https://chromedriver.chromium.org/downloads)) executable compatible with your Chrome browser version.
2. Place the downloaded directory unzipped in a directory that is included in your system's PATH.

### Variables Across Datasets
| Variable | Data Type | DatArt | Electroworld |CZC|
|----------|----------|----------|----------|----------|
| title | string | ✅ | ✅ | ❌ |
| online-retailer | string | ✅ | ✅ | ❌ |
| price | integer (CZK) | ✅ | ✅ | ❌ |
| rating | float | ✅ | ✅ | ❌ |
| number of ratings | int | ✅ | ✅ | ❌ |
| display size | float (inches) | ✅ | ✅ | ❌ |
| resolution width | integer (pixels) | ✅ | ✅ | ❌ |
| connector | string | ✅ | ✅ | ❌ |
| resolution height | integer (pixels) | ✅ | ✅ | ❌ |
| resolution total | integer (pixels) | ✅ | ✅ | ❌ |
| display refresh rate | integer (Hertz) | ✅ | ✅ | ❌ |
| processor manufacturer | string | ✅ | ✅ | ❌ |
| processor model | string | ✅ | ✅ | ❌ |
| number of cores | integer | ✅ | ✅ | ❌ |
| SIM card type | string | ✅ | ✅ | ❌ |
| configuration cards | string | ✅ | ✅ | ❌ |
| degree of protection | string | ✅ | ✅ | ❌ |
| operating system | string | ✅ | ✅ | ❌ |
| internal memory | integer (GB) | ✅ | ✅ | ❌ |
| RAM | integer (GB) | ✅ | ✅ | ❌ |
| charging power | int (Watt) | ✅ | ✅ | ❌ |
| battery capacity | integer (mAh) | ✅ | ✅ | ❌ |
| memory card slot | boolean | ✅ | ✅ | ❌ |
| 4G/LTE | boolean | ✅ | ✅ | ❌ |
| GPS | boolean | ✅ | ✅ | ❌ |
| Wi-Fi | boolean | ✅ | ✅ | ❌ |
| 5G | boolean | ✅ | ✅ | ❌ |
| NFC | boolean | ✅ | ✅ | ❌ |
| Bluetooth | boolean | ✅ | ✅ | ❌ |
| number of rear camera lenses | integer | ✅ | ✅ | ❌ |
| number of front camera lenses | integer | ✅ | ✅ | ❌ |
| rear cam resolution | float (pixels) | ✅ | ✅ | ❌ |
| front cam resolution | float (pixels) | ✅ | ✅ | ❌ |
| fast charging | boolean | ✅ | ✅ | ❌ |
| wireless charging | boolean | ✅ | ✅ | ❌ |
| body fingerprint reader | boolean | ✅ | ✅ | ❌ |
| face unlock | boolean | ✅ | ✅ | ❌ |
| in-display fingerprint reader | boolean | ✅ | ✅ | ❌ |
| 3.5mm jack | boolean | ✅ | ✅ | ❌ |
| FM-radio | boolean | ✅ | ✅ | ❌ |
| colour | string | ✅ | ✅ | ❌ |
| brand | string | ✅ | ✅ | ❌ |
| width | float (cm) | ✅ | ✅ | ❌ |
| length | float (cm) | ✅ | ✅ | ❌ |
| depth | float (cm) | ✅ | ✅ | ❌ |
| volume | float (cubic cm) | ✅ | ✅ | ❌ |
| weight | float (grams) | ✅ | ✅ | ❌ |
| cutout shape | string | ✅ | ❌ | ❌ |
| processor frequency | float (Gigahertz) | ✅ | ❌ | ❌ |
| system superstructure | string | ✅ | ❌ | ❌ |
| notification diode | boolean | ✅ | ❌ | ❌ |
| maximum memory card size | integer | ✅ | ❌ | ❌ |
| Galileo | boolean | ✅ | ❌ | ❌ |
| Beidou | boolean | ✅ | ❌ | ❌ |
| A-GPS | boolean | ✅ | ❌ | ❌ |
| infrared | boolean | ✅ | ❌ | ❌ |
| GLONASS | boolean | ✅ | ❌ | ❌ |
| Bokeh effect | boolean | ✅ | ❌ | ❌ |
| auto focus | boolean | ✅ | ❌ | ❌ |
| thermal camera | boolean | ✅ | ❌ | ❌ |
| wide angle lens | boolean | ✅ | ❌ | ❌ |
| macro mode | boolean | ✅ | ❌ | ❌ |
| night mode | boolean | ✅ | ❌ | ❌ |
| optical zoom | boolean | ✅ | ❌ | ❌ |
| telephoto | boolean | ✅ | ❌ | ❌ |
| hybrid zoom | boolean | ✅ | ❌ | ❌ |
| flash diode | boolean | ✅ | ❌ | ❌ |
| battery type | string | ✅ | ❌ | ❌ |
| removable battery | boolean | ✅ | ❌ | ❌ |
| reverse wireless charging | boolean | ✅ | ❌ | ❌ |
| without fingerprint reader | boolean | ✅ | ❌ | ❌ |
| warranty | int (months) | ✅ | ❌ | ❌ |
| bluetooth version | string | ❌ | ✅ | ❌ |
| WiFi standard | string | ❌ | ✅ | ❌ |
| display type | string | ❌ | ✅ | ❌ |
| resolution label | string | ❌ | ✅ | ❌ |
| display fineness | integer (PPI) | ❌ | ✅ | ❌ |
| smart | boolean | ❌ | ✅ | ❌ |
| water resistant | boolean | ❌ | ✅ | ❌ |
| os brand | string | ❌ | ✅ | ❌ |
| dual SIM support | boolean | ❌ | ✅ | ❌ |
| built-in flash | boolean | ❌ | ✅ | ❌ |
| flash type | string | ❌ | ✅ | ❌ |
| front cam | boolean | ❌ | ✅ | ❌ |
| wireless charging performance | integer (Watt) | ❌ | ✅ | ❌ |
