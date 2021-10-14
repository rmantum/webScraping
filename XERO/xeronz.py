#! Python3

# This program uses requests and BeautifulSoup module to scrape the website " https://www.xero.com/nz/advisors/"
# to extract advisor's Name, Address, Website, PhoneNumber and Status details and save in a CSV.

import csv
import requests
from bs4 import BeautifulSoup

partner = {}
partners = []
profileLinks=[]

host = 'https://www.xero.com/nz/advisors/find-advisors/new-zealand/?type=advisors&orderBy=ADVISOR_RELEVANCE&sort=ASC&pageNumber='

# looping through the page by the numbers
for i in range(1,100):
    url = host+str(i)

    # load the page
    r = requests.get(url)
    if r.ok:  # I we have a ok response
        response = r.text
        page = BeautifulSoup(response, 'lxml')  # Parse through beautifulsoup
        # Find all the profile link from each page and append to the list "profileLinks"
        for link in page.find_all("div",class_="advisors-result-card-view-profile"):
            links = link.find('a')['href']
            profileLinks.append(links)

# for each url in the "ProfileLinks" list
for url in profileLinks:
    r = requests.get(url) # Load prolife page
    if r.ok: # I we have a ok response
        response=r.text

        page = BeautifulSoup(response, 'lxml')  # Parse through beautifulsoup
        name = page.find('h1', class_='advisors-profile-hero-detailed-info-title title-2').text

        try:
            website = page.find('a', class_='btn btn-tertiary-alt advisors-profile-hero-detailed-contact-alt advisors-profile-hero-detailed-contact-website')['href']

        except:
            website = ''

        try:
            phoneNumber = page.find('a', class_='btn btn-tertiary-alt advisors-profile-hero-detailed-contact-alt advisors-profile-hero-detailed-contact-phone')['data-phone']
        except:
            phoneNumber = ''

        try:
            address = page.find('p', class_='advisors-profile-hero-detailed-info-sub national').text
            if '·' in address:
                address = address.split('·')[1]
                address = address.strip()
        except:
            address = ''
        try:
            for item in page.find_all('p', class_="CardHeader__CardPreTitle-sc-1jvagyh-1 xrbFQ PreTitle-sc-1jbmxtl-0 PreTitle gDlsex"):
                if item.text == "Partner status":
                    partnerStatus=item.find_next('h6').text
                    break
            partnerStatus = partnerStatus[:-4]  #slice off the last 4 symble character.
        except:
            partnerStatus = ''
        # Create a Dictionary of the Partner record.
        partner.update({'name': name, 'website': website, 'phoneNumber': phoneNumber, 'address': address, 'partnerStatus': partnerStatus})

        # Append the dictionary records in a list.
        partners.append(dict(partner))

# Write Partners record on a CSV file.
with open('partners.csv', 'w+', newline='') as csvfile:
    fieldnames = ['name', 'website', 'phoneNumber', 'address', 'partnerStatus']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(partners)

