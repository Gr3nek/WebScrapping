from bs4 import BeautifulSoup
import requests
import re

#Wpisywanie rzeczy ktorą chce sie wyszukac
search_term = input("Jakiego produktu szukasz?? ")

#Przypisanie adresu URL
url = f"https://www.newegg.ca/p/pl?d={search_term}&N=4131"
#Pobiera zawartosc strony
page = requests.get(url).text
#Parsuje strone
doc = BeautifulSoup(page, "html.parser")

#Informacje o numerze strony i pobranie elementu strong
page_text = doc.find(class_="list-tool-pagination-text").strong
pages = int(str(page_text).split("/")[-2].split(">")[-1][:-1])

#Słownik, w którym będą przechowywane wyniki 
items_found = {}

#Pętla ze wszystkich stron, która pobiera zawartosć każdej z nich
for page in range(1, pages + 1):
	url = f"https://www.newegg.ca/p/pl?d={search_term}&N=4131&page={page}"
	page = requests.get(url).text
	doc = BeautifulSoup(page, "html.parser")

#Znalezienie elemetu HTML który ma liste wyników, i przeszukanie go
	div = doc.find(class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")
	items = div.find_all(text=re.compile(search_term))

#Pobranie ceny produktu, usunięcie przecinków, zapisanie ceny i url w słowniku
	for item in items:
		parent = item.parent
		if parent.name != "a":
			continue

		link = parent['href']
		next_parent = item.find_parent(class_="item-container")
		try:
			price = next_parent.find(class_="price-current").find("strong").string
			items_found[item] = {"price": int(price.replace(",", "")), "link": link}
		except:
			pass

sorted_items = sorted(items_found.items(), key=lambda x: x[1]['price'])

for item in sorted_items:
	print(item[0])
	print(f"${item[1]['price']}")
	print(item[1]['link'])
	print("-------------------------------")







