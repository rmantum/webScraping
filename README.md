# webScraping
This repository will contain various web scraping solutions

# NZCB:
- This program uses requests and BeautifulSoup module to scrape the website "https://www.nzcb.nz/find-your-builder/"
- To extract Business Name, Website, PhoneNumber and Representative and save in a CSV nzcb.csv.

# xeronz:
- This program uses requests and BeautifulSoup module to scrape the website " https://www.xero.com/nz/advisors/"
- To extract advisor's Name, Address, Website, PhoneNumber and Status details and save in a CSV.

# MFAA:
- This script reads a postcode.csv file and loads target postcodes in a dataframe. 
- Then it goes in the website "https://www.mortgageandfinancehelp.com.au/find-accredited-broker/?location=" and load pages by postcodes.
- It then loads each partner profile page and scrape 'id', 'full_name', 'prefered_name', 'last_name', 'email', 'mobile', 'phone', 'company', 'suburb', 'postcode', 'state'
- The script then save these details in a csv.
