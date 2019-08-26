import requests
import os
from bs4 import BeautifulSoup
import re

url = r'https://www.geeksforgeeks.org/computer-network-tutorials/?fbclid=\
        IwAR3HIUxFznzdogs0nlbsy72ctJQG8JRdDVYXpfs2h1805bf75bnfHpP7mmE#dll'

request_object = requests.get(url)
soup = BeautifulSoup(request_object.text, 'html.parser')

style_titles = ['width: 50%;float: left;text-align: left',
                'width: 50%;float: right;text-align: left'] # Style Tags from page

headers = []  # Basic DataLink da ash.
class_titles = []  # Href for Parsing Each Section
chapter_titles = [] # Title for each chapter
all_urls = []

def headers_classtitles(style_list):
    for styleclass in style_list:
        for i in soup.find_all('div', style=styleclass):
            for ultag in i.find_all('ul'):
                for litag in ultag.find_all('li'):
                    for a in litag.find_all('a'):
                        headers.append(a.get_text())
                        class_titles.append(str(a['href'].replace('#', ''))) if len(
                            str(a['href'])) > 1 else class_titles.append('misc')
                        
    

headers_classtitles(style_titles)

def get_urls_and_titles(classname):
    for name in classname:
        for item in soup.find_all('div', class_=name):
            for ol in item.find_all('ol'):
                for li in ol.find_all('li'):
                    for a in li.find_all('a'):
                        all_urls.append(str(a['href']))
                        chapter_titles.append((a.get_text() + '.html'))
                        break
get_urls_and_titles(class_titles)

