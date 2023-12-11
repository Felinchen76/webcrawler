from urllib.parse import urljoin

import tkinter as tk

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

import requests
import time
from bs4 import BeautifulSoup



# verwendete URLS zum crawlen
url = 'https://technical.city/de/video'
url_price_comparison = 'https://geizhals.de/?o=8'


def find_cheapest(graca_prices):
    return min(graca_prices)

def get_all_prices(graca_price_comparison_url):
    results = get_website_content(graca_price_comparison_url)
    soup = print_website_content(results)
    graca_prices = []
    tabs = soup.find_all('a', class_='gh_pag_i only--desktop', href=True)
    prices = []
    for tab in tabs:
        link = urljoin(url_price_comparison, str(tab))
        tab_content = get_website_content(link)
        tab_soup = print_website_content(tab_content)
        prices = tab_soup.find_all('span', class_='price')

    for price in prices:
        graca_prices.append(price.text)
    print(graca_prices)


def send_http_request(top_gracas):
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get(url_price_comparison)
    time.sleep(3)

    action = driver.find_element(By.XPATH,'//*[@id="fs"]')
    action.send_keys(top_gracas[0])
    action.submit()
    current_url = driver.current_url
    time.sleep(10)
    driver.quit()
    return current_url

def get_website_content(url):
    # hier wird Markdown der Website gespeichert
    results = requests.get(url)
    return results


def print_website_content(html_content):
    # print Content of website
    soup = BeautifulSoup(html_content.text, "html.parser")
    print(soup.prettify())
    return soup


def get_top_graca(soup):
    # liste mit den 5 besten Grafikkarten aktuell auf dem Markt, laut der Website
    top_graca = []
    top_graca_div = soup.find_all('strong', class_='title')
    print(top_graca_div)
    for container in top_graca_div:
        graca_name = container.a.text
        top_graca.append(graca_name)
    return top_graca

def on_button_click():
    top_gracas_content = get_website_content(url)
    soup = print_website_content(top_gracas_content)
    top_gracas = get_top_graca(soup)
    graca_price_comparison_url = send_http_request(top_gracas)

    get_all_prices(graca_price_comparison_url)


# GUI erstellen
window = tk.Tk()
window.title("GRAKAS")

# button erstellen
button = tk.Button(window, text="Crawl Gracas!", command=on_button_click)
button.pack(pady=10)

# Erstelle ein Textausgabefeld
text_output = tk.Text(window, width=40, height=10, state=tk.DISABLED)
text_output.pack(pady=10)

# Starte die GUI-Schleife
window.mainloop()