import requests
from bs4 import BeautifulSoup as bfs
def link_scrapper():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    ofset = 0
    all_restaurent_links = []

    while True:
        try:
            if ofset<=29:
                url = 'https://www.tripadvisor.com/Restaurants-g181718-Coquitlam_British_Columbia.html'
                
            else:
                # https://www.tripadvisor.com/Search?q=Burnaby&searchSessionId=42CBB6AE2C7440C68DCCD0FF703B8D121704436847955ssid&sid=A4D0676588FE4BD7821F7180CE9D215F1704436850944&blockRedirect=true&geo=1&ssrc=e&rf=7&o=30{ofset}
                url = f'https://www.tripadvisor.com/Search?q=Burnaby&searchSessionId=42CBB6AE2C7440C68DCCD0FF703B8D121704436847955ssid&sid=A4D0676588FE4BD7821F7180CE9D215F1704436850944&blockRedirect=true&geo=1&ssrc=e&rf=7&o={ofset}'
            
            print(url)
            all_restaurant_page = requests.get(url, headers=headers, timeout=10)
            try:
                if all_restaurant_page.status_code == 200:
                    source = bfs(all_restaurant_page.content, 'html.parser')
                    current_links = []
                    for link in source.find_all('a', href=True):
                        if "Restaurant_Review" in link['href'] and 'html#REVIEWS' not in link['href']:
                            full_link = "https://www.tripadvisor.com" + link['href']
                            current_links.append(full_link)
                    current_links = list(set(current_links))
                    print(f"got {len(current_links)}restaurant links")
                    with open('all_restaurent_links.txt', "a") as file:  # Use "a" mode to append
                        for restaurant in current_links:
                            file.write(restaurant + "\n")

                    ofset = ofset+30
            except Exception as e:
                print(e)
                    



            program = 'running'
        except requests.Timeout:
            print("The request timed out!")
        except requests.RequestException as e:
            print(f"An error occurred: {e}")

