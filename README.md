# Preamble
This program will scrap the dynamic HTML table from eGP system. The scrapper will only use what is publicly available on the internet and it does not require any elevated credentials. Further, it does not impact the stability of the website in any way and does not affect others from accessing the web. The scrappers uses built-in delay to avoid bombarding the system server with HTTP request besides allowing the webpage adequate time to load all assets.

# Background
The [eGP system](https://www.egp.gov.bt/) is established to promote transparency and efficiency in public procurement process which can ultimately build good governance in Bhutan. Thus, all agencies in the country use this system. Users can view public tenders on the website without requiring any login credentials. 

# Objectives
This Python app is built to 
a. Scrap public procurement data scrapped from the eGP website
b. Use the data to study procurement trends
c. Perform other statistical analysis to derive other 'meanings' from the data

# Dependencies
It uses `pandas`, `selenium` and `webdriver_manager` packages.

# Disclaimer
This project does not belong to any government agencies or is not intended to be. It only shall serve the purpose of learning and extracting meaning from data. 

# Contribution
You may contribute to this project on my [Github page](https://github.com/UgyenNorbu/eGP_scrapper) or on my profile on [Datascienceportfolio.io](https://www.datascienceportfol.io/ugyen_norbu).