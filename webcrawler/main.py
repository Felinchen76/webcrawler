import PySimpleGUI as sg
import queue
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

# GUI erstellen
window = sg.Window(title="GRAKA Crawler", layout=[
    [sg.Text('Search for best price graphic card model xyz', justification='center')],
    [sg.Button('Crawl')]],
    margins=(300, 150))

url = 'https://duckduckgo.com/?q=grafikkarten+kaufen&ia=web'

queue = queue.Queue()
limit = 500
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

def get_blog_content(url):
    try:
        #set_playwright_browsers_path()
        driver.get(url)

        articles = driver.find_elements(By.CLASS_NAME,'wLL07_0Xnd1QZpzpfR4W')

        for article in articles:
            #vllt bietet sich hier was anderes mehr an...? -> ich muss ja nun auch auf anderen Seiten suchen können
            link = article.find_element(By.XPATH,'..//div[2]/h2/a').get_attribute('href')
            print('Link: %s' % link)
            if queue.qsize() < limit:
                if 'youtube' not in link:
                    queue.put(link)

    except Exception as e:
        print(f'Fehler beim Verarbeiten der URL {url}: {e}')
    finally:
        # Schließe den Browser
        driver.quit()
def main():
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break
        elif event == "Crawl":
            get_blog_content(url)

    window.close()

main()
