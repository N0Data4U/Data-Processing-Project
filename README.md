# Data-Processing-Project

This final project is part of the Data Processing in Python (JEM207) course at IES.
This project is about scraping, procesing and, analysis mobile phone data, utilizing the python programming language.
Precisely, we scrape data from three Czech online retailers using the BeautifulSoup library. During the data processing 
stage we try to transform data from multiple sources into a uniform format. Finally, multiple phone characteristics are 
used to draw coclusions about the phone prices.



<img width="1054" alt="Screenshot 2024-01-17 at 19 10 50" src="https://github.com/N0Data4U/Data-Processing-Project/assets/126565081/23ec8197-236d-4b82-b34d-1edf0e221eb3">

## Runnability  
### main.py
The "main.py" file includes the whole pipeline from scraping and processing the data to data integration and data analysis. 
Only this file needs to be executed.
### ChromeDriver Installation
1. Download the [ChromeDriver]([https://sites.google.com/chromium.org/driver/](https://chromedriver.chromium.org/downloads)) executable compatible with your Chrome browser version.
2. Place the downloaded directory unzipped in a directory that is included in your system's PATH.

### Variables Across Datasets
| Variable | Data Type | DatArt | Electroworld |
|----------|----------|----------|----------|
| title | string | ✅ | ✅ |
| online-retailer | string | ✅ | ✅ |
| price | integer (CZK) | ✅ | ✅ |
| rating | float | ✅ | ✅ |
| number of ratings | int | ✅ | ✅ |
| display size | float (inches) | ✅ | ✅ |
| resolution width | integer (pixels) | ✅ | ✅ |
| connector | string | ✅ | ✅ |
| resolution height | integer (pixels) | ✅ | ✅ |
| resolution total | integer (pixels) | ✅ | ✅ |
| display refresh rate | integer (Hertz) | ✅ | ✅ |
| processor manufacturer | string | ✅ | ✅ |
| processor model | string | ✅ | ✅ |
| number of cores | integer | ✅ | ✅ |
| SIM card type | string | ✅ | ✅ |
| configuration cards | string | ✅ | ✅ |
| degree of protection | string | ✅ | ✅ |
| operating system | string | ✅ | ✅ |
| internal memory | integer (GB) | ✅ | ✅ |
| RAM | integer (GB) | ✅ | ✅ |
| charging power | int (Watt) | ✅ | ✅ |
| battery capacity | integer (mAh) | ✅ | ✅ |
| memory card slot | boolean | ✅ | ✅ |
| 4G/LTE | boolean | ✅ | ✅ |
| GPS | boolean | ✅ | ✅ |
| Wi-Fi | boolean | ✅ | ✅ |
| 5G | boolean | ✅ | ✅ |
| NFC | boolean | ✅ | ✅ |
| Bluetooth | boolean | ✅ | ✅ |
| number of rear camera lenses | integer | ✅ | ✅ |
| number of front camera lenses | integer | ✅ | ✅ |
| rear cam resolution | float (pixels) | ✅ | ✅ |
| front cam resolution | float (pixels) | ✅ | ✅ |
| fast charging | boolean | ✅ | ✅ |
| wireless charging | boolean | ✅ | ✅ |
| body fingerprint reader | boolean | ✅ | ✅ |
| face unlock | boolean | ✅ | ✅ |
| in-display fingerprint reader | boolean | ✅ | ✅ |
| 3.5mm jack | boolean | ✅ | ✅ |
| FM-radio | boolean | ✅ | ✅ |
| colour | string | ✅ | ✅ |
| brand | string | ✅ | ✅ |
| width | float (cm) | ✅ | ✅ |
| length | float (cm) | ✅ | ✅ |
| depth | float (cm) | ✅ | ✅ |
| volume | float (cubic cm) | ✅ | ✅ |
| weight | float (grams) | ✅ | ✅ |
| cutout shape | string | ✅ | ❌ |
| processor frequency | float (Gigahertz) | ✅ | ❌ |
| system superstructure | string | ✅ | ❌ |
| notification diode | boolean | ✅ | ❌ |
| maximum memory card size | integer | ✅ | ❌ |
| Galileo | boolean | ✅ | ❌ |
| Beidou | boolean | ✅ | ❌ |
| A-GPS | boolean | ✅ | ❌ |
| infrared | boolean | ✅ | ❌ |
| GLONASS | boolean | ✅ | ❌ |
| Bokeh effect | boolean | ✅ | ❌ |
| auto focus | boolean | ✅ | ❌ |
| thermal camera | boolean | ✅ | ❌ |
| wide angle lens | boolean | ✅ | ❌ 
| macro mode | boolean | ✅ | ❌ |
| night mode | boolean | ✅ | ❌ |
| optical zoom | boolean | ✅ | ❌ |
| telephoto | boolean | ✅ | ❌ |
| hybrid zoom | boolean | ✅ | ❌ |
| flash diode | boolean | ✅ | ❌ |
| battery type | string | ✅ | ❌ |
| removable battery | boolean | ✅ | ❌ |
| reverse wireless charging | boolean | ✅ | ❌ |
| without fingerprint reader | boolean | ✅ | ❌ |
| warranty | int (months) | ✅ | ❌ |
| bluetooth version | string | ❌ | ✅ |
| WiFi standard | string | ❌ | ✅ |
| display type | string | ❌ | ✅ |
| resolution label | string | ❌ | ✅ |
| display fineness | integer (PPI) | ❌ | ✅ |
| smart | boolean | ❌ | ✅ |
| water resistant | boolean | ❌ | ✅ |
| os brand | string | ❌ | ✅ |
| dual SIM support | boolean | ❌ | ✅ |
| built-in flash | boolean | ❌ | ✅ |
| flash type | string | ❌ | ✅ |
| front cam | boolean | ❌ | ✅ |
| wireless charging performance | integer (Watt) | ❌ | ✅ |

### Data Analysis
The main focus lies on the price variable. For simple analysis some typical summary statistics were calculated for the price variable and some other interesting characteristics. The complete data set, consisting of data from two sources DatArt and Electroworld, contains 1687 rows and 48 variables. 
The prices of mobile phones vary between 449 and 53990 crowns with a mean 12140,03 crowns, giving a first hint for right-skewness (see table below). Most metric variables contain less than 100 NA's and therefore serves as variables for price modelling. An exception is the variable rating with more than 500 NA's. 
#### Graph 1
![Graph 1](images/metric_variables_table.png)

This is a description of Graph 1.

#### Graph 2
![Graph 2](images/online_retailer_table.png)

In total there are 950 (736) products included from DatArt (Electroworld). 

#### Graph 3
![Graph 3](images/brand_table.png)

Most of the products belong to Apple (19%) followed by Samsung (17,7%) and Xiaomi (13,5%).

#### Graph 4
![Graph 4](images/online_retailer_comp.png)

Some grouped metrics were calculated for the retailers. The average price of mobile phones does not vary much between the two retailers and lies around 12000 crowns. Further, the company with the most supplied products on the websites is apple in both cases. The most supplied colour of a phone is black in both cases. However, the number of ratings is much higher for DatArt (20058) than for Electroworld (1816), given a hint that the first website is used more often for buying phones.

#### Graph 5
![Graph 5](images/bar_plots_grouped.png)

The brands are allocated quite similar for both websites. However, Electroworld supplies Samsung more often than Xiaomi phones compared to DatArt. The colours and degrees of protection are also allocated quite equally. DatArt offers many products with a processor manufacturered by Qualcomm and Electroworld by Mediathek Helio. For this variable noticable differences can be found.

#### Graph 6
![Graph 6](images/pie_plots.png)

More than half of all products include no wireless charging (64,6%) and the most supplied connector for phones is USB-c (75,4%).

#### Graph 7
![Graph 7](images/scatter_plots_brand)

Prices seem to have a slight positive association with the rear cam resolution. However, there are also some products with a very high rear cam resolution but a more average price. In this association there seems to be no big difference between the two websites. The volume of a product seems to have almost no influence on prices. It is comparably low for high and low price phones.

#### Graph 8
![Graph 8](images/scatter_plots_brand.png.png)

There seems to be a positive relationship between prices and display size. 
Also between the variables resolution (resolution width x resolution height) and price seems to be a positive relationship.

#### Graph 9
![Graph 9](images/pie_plots.png)

This is a description of Graph 9.

#### Graph 10
![Graph 10](images/pie_plots.png)

This is a description of Graph 10.

#### Graph 11
![Graph 11](images/pie_plots.png)

This is a description of Graph 11.

#### Graph 12
![Graph 12](images/pie_plots.png)

This is a description of Graph 12.

#### Graph 13
![Graph 13](images/pie_plots.png)

This is a description of Graph 13.

#### Graph 14
![Graph 14](images/pie_plots.png)

This is a description of Graph 14.

#### Graph 15
![Graph 15](images/pie_plots.png)

This is a description of Graph 15.