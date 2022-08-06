from bs4 import BeautifulSoup
import requests
import re
import json
import os

NUM_AJAX_PAGE = 10
# quote_page = "https://tiki.vn/api/v2/products?limit=48&include=advertisement&aggregations=1&trackity_id=4956f93e-b53b-7e5e-51f4-590744d24a1b&category=316&page={page}&src=c.316.hamburger_menu_fly_out_banner&urlKey=sach-truyen-tieng-viet"
quote_page = "https://tiki.vn/api/personalish/v1/blocks/listings?limit=48&include=advertisement&aggregations=2&trackity_id=800a52ee-b1d4-9b6b-2306-a5371ec7e519&category=8322&page=1&urlKey=nha-sach-tiki"
api_page = "https://tiki.vn/api/v2/products/{id}"
headers = {'user-agent':'Mozilla/5.0'}
product_id_folder = os.getcwd() + "/products/id/"
product_json_folder = os.getcwd() + "/products/json/"

def get_product_id():
    product_list = []
    i = 1
    while (i < NUM_AJAX_PAGE):
        print("Crawling id from page:", i, end=" ")
        response = requests.get(quote_page.format(page=i),headers=headers,data={})
        data = json.loads(response.text)
        print("with %d products" % len(data["data"]))
        product_box = []
        for data in data.get("data"):
            product_list.append(data["id"])
        i += 1

        # page = requests.request('GET',url,headers=headers)
        # soup = BeautifulSoup(page.content,"html.parser")
        # name_box = soup.find('div', attrs={'class':'ProductList__Wrapper-sc-1dl80l2-0 healEa'})
        # for paragraph in name_box.find_all('a',href=True):
        #         match = re.findall(r"\/*(p\d+)", str(paragraph.get('href')))
        #         new_id_string = match[0].replace("p","")
        #         list_of_id.append(new_id_string)
    return product_list, i
    

def write_id_to_txt(list_of_id=[]):
    file_path = product_id_folder + 'id.txt'
    with open(file_path, 'w') as f:
        for id in list_of_id:
            f.write("%s\n" % id)

def crawl_product_from_id(list_of_id=[]):
    list_of_products = []
    for id in list_of_id:
        print("Crawling id: ",id)
        crawl_page = api_page.format(id=id)
        page = requests.get(crawl_page, headers=headers)
        if page.content:
            list_of_products.append(page.json())
    return list_of_products

def write_products_to_json_file(list_of_products=[]):
    keys = [
        'id','sku','name','categories','short_description','description','price','list_price','discount',\
        'productset_group_name','specifications','thumbnail_url','publisher','authors','stock_item',\
        'rating_average','review_count'
    ]
    for product in list_of_products:
        new_dict_product = {}
        if not product.get("id", False):
            new_dict_product = {}
        else:
            print("Writing product %d to file json..." % product['id'])
            product['thumbnail_url'] = product['thumbnail_url'].replace('280x280','w1200')
            file_path = product_json_folder + str(product['id']) + ".json"
            new_dict_product = dict((key, product[key]) for key in keys if key in product)
            f = open(file_path, 'w')
            json.dump(new_dict_product, f, ensure_ascii=False, indent=4)
            f.close()
        


if __name__ == "__main__":
    list_of_id, number_of_page = get_product_id()
    write_id_to_txt(list_of_id)
    list_of_products = crawl_product_from_id(list_of_id)
    write_products_to_json_file(list_of_products)
    print('='*80)
    print("Crawling process finished")
    print("No. pages: ",number_of_page)
    print("No. products: ",len(list_of_products))




