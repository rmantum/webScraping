#! python3

# This script reads a postcode.csv file and loads target postcodes in a dataframe. 
# Then it goes in the website "https://www.mortgageandfinancehelp.com.au/find-accredited-broker/?location=" and load pages by postcodes.
# It then loads each partner profile page and scrape 'id', 'full_name', 'prefered_name', 'last_name', 'email', 'mobile', 'phone', 'company', 'suburb', 'postcode', 'state'
# The script then save these details in a csv.

import csv
import pandas as pd
import requests
from bs4 import BeautifulSoup




def loadsite(url, headers, cookies):
    # Load the homepage using requests module
    r = requests.get(url,headers=headers)
    if r.ok:
        response = r.text
        return response
    else:
        print('page load error............')
        return none

postcodes = pd.read_csv('postcodes.csv')





brokers = []

headers={'authority':'www.mortgageandfinancehelp.com.au',
'Accept':'*/*',
'x-requested-with':'XMLHttpRequest',
'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
'sec-fetch-site': 'same-origin',
'sec-fetch-mode': 'cors',
'Referer': 'https://www.mortgageandfinancehelp.com.au/find-accredited-broker/?speciality=Business&location=2565',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'}

for item in postcodes['postcode']:
    code = str(item)
    postcode = code.zfill(4)


    class BreakIt(Exception):
        pass

    class BreakIt2(Exception):
        pass

    check = True
    page_number = 1
    while page_number and check:
        check = False
        url = 'https://www.mortgageandfinancehelp.com.au/find-accredited-broker/?page='+str(page_number)+'&query=&location='+ postcode +'&expertise=Business'
        print(url)
        page_number += 1
        response = loadsite(url, headers, cookies='')

        page = BeautifulSoup(response, 'lxml')
        # print(page.prettify())
        try:
            for broker_html in page.find_all('div', class_="broker col-lg-4 col-md-6 col-xs-12"):
            # print(broker_html.prettify())
                check = True
                broker = dict.fromkeys(
                    ['id', 'full_name', 'prefered_name', 'last_name', 'email', 'mobile', 'phone', 'company', 'suburb', 'postcode', 'state'])

                id = broker_html.find('a', class_="viewdetails_button standard")['data-external_id']


                for ids in brokers:
                    if id == ids['id']:
                        raise BreakIt

                try:
                    full_name = broker_html.find('h2', class_="broker-name").text
                except:
                    full_name = ''
                try:
                    prefered_name = broker_html.find('a', class_="viewdetails_button standard")['data-preferred_name']
                except:
                    prefered_name = ''
                try:
                    last_name = broker_html.find('a', class_="viewdetails_button standard")['data-last_name']
                except:
                    last_name = ''
                try:
                    email = broker_html.find('a', class_="viewdetails_button standard")['data-email']
                except:
                    email = ''
                try:
                    mobile = broker_html.find('a', class_="viewdetails_button standard")['data-mobile']
                except:
                    mobile = ''
                try:
                    phone = broker_html.find('a', class_="viewdetails_button standard")['data-phone']
                except:
                    phone = ''
                try:
                    company = broker_html.find('a', class_="viewdetails_button standard")['data-company']
                except:
                    company = ''
                try:
                    suburb = broker_html.find('a', class_="viewdetails_button standard")['data-city']
                except:
                    suburb = ''
                try:
                    state = broker_html.find('a', class_="viewdetails_button standard")['data-state']
                except:
                    state = ''

                broker.update({'full_name':full_name, 'id':id, 'prefered_name':prefered_name, 'last_name':last_name, 'email':email, 'mobile':mobile, 'phone':phone, 'company':company, 'suburb': suburb, 'postcode': postcode, 'state':state})
                # print(full_name + '\n' + id + '\n' + prefered_name + '\n' + last_name + '\n' + email + '\n' + mobile + '\n' + phone + '\n' + company + '\n' + suburb + '\n' + state)
                brokers.append(dict(broker))


        except BreakIt:
            print('breakit : '+str(page_number)+'postcode:'+str(postcode))
            page_number = False
            break



# Write Partners record on a CSV file.
with open('brokerlist_nt.csv', 'w+', newline='') as csvfile:
    fieldnames = ['id', 'full_name', 'prefered_name', 'last_name', 'email', 'mobile', 'phone', 'company', 'suburb', 'postcode', 'state']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(brokers)