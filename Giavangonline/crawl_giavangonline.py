from bs4 import BeautifulSoup
import requests
import time
import json
import os
from datetime import date, timedelta, datetime

NUM_AJAX_PAGE = 22
quote_page = "https://giavangonline.com/goldhistory.php?date="
headers = {'user-agent':'Mozilla/5.0'}
gold_price_folder = os.getcwd() + "/gold_price/"
gold_price_file_name = "gold_price.json"

def crawl_gold_price():
    crawling_date = datetime.strptime('2011-01-01', '%Y-%m-%d').date()
    today = date.today()
    current_quote_page = quote_page + str(crawling_date)
    dict_of_gold_price = list()
    while(crawling_date != (today + timedelta(days=1))):
        print("Crawling date:", crawling_date)
        page = requests.request('GET',current_quote_page,headers=headers)
        soup = BeautifulSoup(page.content,"html.parser")
        table_box = soup.find('table', attrs={'class':'home'})
        sjc_box = soup.find_all('td', attrs={'class':'col-left'})
        price_box = soup.find_all('td', attrs={'class':'center'})
        if len(sjc_box) == 0 and len(price_box) == 0:
            print("There is no data on this date")
        if len(sjc_box) != len(price_box):
            print("There is an error in table format")
            break
        else:
            for i in range(len(sjc_box)):
                new_dict = {}
                new_dict['date'] = str(crawling_date)
                new_dict['sjc'] = sjc_box[i].text
                new_dict['price'] = price_box[i].text
                dict_of_gold_price.append(new_dict)
                
        crawling_date += timedelta(days=1)
        current_quote_page = quote_page + str(crawling_date)

    
    return dict_of_gold_price

def generate_json_file(list_of_products=[]):
    file_path = gold_price_folder + gold_price_file_name
    f = open(file_path, 'w')
    json.dump(list_of_products, f, ensure_ascii=False, indent=4)
    f.close()

dict_of_gold_price = crawl_gold_price()
generate_json_file(dict_of_gold_price)
print(dict_of_gold_price)