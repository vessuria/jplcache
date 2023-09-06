import re
import requests
from bs4 import BeautifulSoup
import pandas

def transformUrl(src: str):
    address = re.sub('(?=\.2e).*(?=.jpg)', '', src)
    address = re.sub('/images/', '/original_images/', address)
    return address
    

def main():
    count = 0
    data = pandas.DataFrame(columns=['Count', 'Text', 'Url'])
    
    for page in range(1, 835):
        items = 0
        url = f'https://www.jpl.nasa.gov/images?page={page}'
        content = BeautifulSoup(requests.get(url).content, 'html.parser').find_all('li')
        for li in content:
            text = li.find('span').text.strip()
            url = transformUrl(li.find('img')['data-src'])
            
            data.loc[len(data.index)] = [count, text, url]
            count++
            items++
        
        print(f'Page {page}: Fetched {items} URLs [{count}]')
        
    data.to_csv('image-urls.csv', header=False, index=False)
    print(f'Process complete! Saved {count} URLs')

main()
