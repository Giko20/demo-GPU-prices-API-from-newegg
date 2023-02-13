from bs4 import BeautifulSoup
import requests
import re
import json

search_item = input("What GPU number do you want? ")

filename = input("Enter json filename: ")

url = f"https://www.newegg.com/p/pl?d={search_item}&N=4131"

page = requests.get(url).text

doc = BeautifulSoup(page, "html.parser")

page_text = doc.find(class_ = "list-tool-pagination-text").strong

pages = int(str(page_text).split("/")[-2].split(">")[-1][:-1])

items_found = {}
# json_format = {}


for page in range(1, pages + 1):
    url = f"https://www.newegg.com/p/pl?d={search_item}&N=4131&page={page}"
    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")
    
    div = doc.find(class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")
    items = div.find_all(text=re.compile(search_item))
        
    for item in items:
        parent = item.parent
        if parent.name != "a":
            continue
        link = parent["href"]
        next_parent = item.find_parent(class_="item-container")
        price_div = next_parent.find(class_="price-current").strong
        suffix = next_parent.find(class_="price-current").sup
        if price_div == None:
            continue
        price_index = price_div.string
        price_suffix = suffix.string
        price = float(str(price_index.replace(",", "")) + str(price_suffix))
        items_found[item] = {'price':price, 'link':link}

sorted_items = sorted(items_found.items(), key=lambda x: x[1]["price"])

first = []
second = []
third = []

for item in sorted_items:
    first.append(item[0])
    second.append(f"${item[1]['price']}")
    third.append(item[1]['link'])

json_format = {'name': first, 'prices':second, 'links':third}

with open(filename + '.json', 'w', encoding='utf-8') as f:
    json.dump(json_format, f, ensure_ascii=False, indent=4)
