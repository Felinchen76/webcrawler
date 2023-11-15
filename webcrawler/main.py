#wieso geht das???
#selenium für das laden dynamischer inhalte
import bs4
from bs4 import BeautifulSoup
import requests
import cssutils
import queue

url = 'https://de.wikipedia.org/wiki/Schwarzes_Loch'
queue = queue.Queue()
limit = 500

def get_url_content(url):
    return requests.get(url).text

def get_blog_content(url):
    content = get_url_content(url)
    soup = BeautifulSoup(content, "html.parser")

    #einfach alle Links von der Seite ziehen
    for post in soup.findAll('a'):
        #damit nur die eigentlichen Linktexte ausgegeben werden und nicht die tags ebenfalls
        link = post.get('href')
        print('Link: %s' % link)
        if queue.qsize() < limit:
            queue.put(link)

get_blog_content(url)

while queue.qsize() != 0:
    try:
        get_blog_content(queue.get())
        limit = limit - 1
    except Exception:
        print('no valid url')