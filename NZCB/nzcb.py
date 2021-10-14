#! Python3

# This program uses requests and BeautifulSoup module to scrape the website "https://www.nzcb.nz/find-your-builder/"
# to extract Business Name, Website, PhoneNumber and Representative and save in a CSV.

import csv
import requests
from bs4 import BeautifulSoup

def main(host):
    business = {}
    businesses = []
    profileLinks = []

    # looping through the page by the numbers
    for i in range(1, 2):
        url = host + str(i)

        # load the page
        r = requests.get(url)
        if r.ok:  # I we have a ok response
            response = r.text
            page = BeautifulSoup(response, 'lxml')  # Parse through beautifulsoup

            # Find all the profile link from each page and append to the list "profileLinks"
            for link in page.find_all("h2", class_="elementor-heading-title elementor-size-default"):
                links = link.find('a')['href']
                profileLinks.append(links)
    print(len(profileLinks))

    # for each url in the "ProfileLinks" list
    for url in profileLinks:
        r = requests.get(url)  # Load prolife page
        if r.ok:  # I we have a ok response
            response = r.text

            page = BeautifulSoup(response, 'lxml')  # Parse through beautifulsoup

            name = page.find('h2', class_='elementor-heading-title elementor-size-default').text

            try:
                rep = page.find('div',
                                class_="elementor-element elementor-element-8847595 elementor-align-left elementor-icon-list--layout-traditional elementor-widget elementor-widget-icon-list")

                reps = rep.findAll('li')

                representative = reps[1].span.text
                representative = representative.replace('Representative', '')

            except:
                representative = ''

            try:
                website = page.find('div',
                                    class_='elementor-element elementor-element-e7e8582 elementor-align-left elementor-icon-list--layout-traditional elementor-widget elementor-widget-icon-list').a[
                    'href']
            except:
                website = ''

            try:
                phoneNumber = page.find('div', id='nzcb-business-phone-hidden').a['href']
            except:
                phoneNumber = ''

            # Create a Dictionary of the Business record.
            business.update(
                {'name': name, 'representative': representative, 'website': website, 'phoneNumber': phoneNumber})

            # Append the dictionary records in a list.
            businesses.append(dict(business))

    # Write Business record on a CSV file.
    with open('nzcb2.csv', 'w+', newline='') as csvfile:
        fieldnames = ['name', 'representative', 'website', 'phoneNumber']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(businesses)

if __name__ == '__main__':
    main('https://www.nzcb.nz/find-your-builder/')


