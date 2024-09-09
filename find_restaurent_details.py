import re
import requests
from bs4 import BeautifulSoup as bfs
from append_data_to_excel import append_excel_sheet_data

def find_restaurant_details():
    restaurant_links = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }



    # Open the file in read mode and read each line
    with open('final_restaurent_links.txt', 'r') as file:
        for line in file:
            # Strip the newline character from the end of each line and append to the list
            restaurent_link = line.strip()
            done_restaurant_links = []
            # Open the file in read mode and read each line
            with open('done_restaurent_links.txt', 'r') as file:
                for line in file:
                    # Strip the newline character from the end of each line and append to the list
                    done_restaurant_links.append(line.strip())

            if restaurent_link not in done_restaurant_links:
                print(f'Working on {restaurent_link}')
                restaurent_page = requests.get(restaurent_link, headers=headers, timeout=20)
                restaurant_page_source = bfs(restaurent_page.content, 'html.parser')

                header_tag = restaurant_page_source.find('h1', {'data-test-target': 'top-info-header'})
                restaurant_name = header_tag.string

                map_address = restaurant_page_source.find('a', {"href": '#MAPVIEW'})
                map_address = map_address.string
                email = ''
                for link in restaurant_page_source.find_all('a', href=True):
                    if "tel:" in link['href']:
                        phone_number = link['href'].replace('tel:', '')
                        break
                for link in restaurant_page_source.find_all('a', href=True):
                    if "mailto:" in link['href']:
                        email = link['href'].replace('mailto:', '')
                        email = email.replace('?subject=?', '')
                        break   
                
                item = {
                    'Restaurant_Name': restaurant_name,
                    'Email': email,
                    'Phone': phone_number,
                    'Address': map_address
                }
                print(item)
                append_excel_sheet_data(item)
                print('==========================================================================')
                with open('done_restaurent_links.txt', "a") as file:  # Use "a" mode to append
                    file.write(restaurent_link + "\n")