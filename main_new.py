import os
import sys
import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
import re
from time import sleep
import json
import glob2

from time import sleep
import time
import concurrent.futures
import threading

start_time = time.time()
try:
    css_file = glob2.glob('*.css')[0]
except:
    pass
rel = "stylesheet"
tagname = "style"
__style = r"""

      body {
        margin: 30 !important;
      }

      h1 {
        text-align: center;
        font-size: xx-large !important;
        color: red;
      }
    

"""


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def directory_staff():
    "creates directory for all html files which will download"
    if not os.path.isdir("network"):
        os.mkdir("network")


def make_request(url):
    "Makes Http request and Return BeautifulSoup Object"
    try:
        print(f"{bcolors.OKGREEN}Making GET request to {url} ---{bcolors.ENDC}")
        response = requests.get(url)
        response.raise_for_status()
        print(f"{bcolors.OKBLUE}Response status {response.status_code}{bcolors.BOLD}")
        return BeautifulSoup(response.text, 'lxml')
    except:
        print("HTTP ERROR or Url not found")
        return None


def make_style_tag(bsObj, tagname, style):
    "Creates new html link tag for css file"
    soup = bsObj
    style_tag = soup.new_tag(tagname)
    style_tag.string = style
    return style_tag


def get_titles(bsObj):
    "Return list of all titles"
    domain = 'https://www.geeksforgeeks.org/'
    ctr = 0
    print("Downloading some dependencies")
    if bsObj != None:
        sides = ['left', 'right']
        soup = bsObj
        pages = set()
        chapters = []

        for side in sides:
            for title in soup.find("div", {"style": f"width: 50%;float: {side};text-align: left"}).find_all('a'):
                if 'href' in title.attrs:

                    chapters.append(title.attrs['href'].replace("#", '')) if len(
                        str(title.attrs['href'])) > 1 else chapters.append('misc')
        index = chapters.index('nsc')
        chapters[index] = 'tl'
        return chapters
    else:
        print("Somthing Went Wrong")
        return None


def get_Links(titles, soup):
    """Aburnebs yvela Tavis(chapter) Urls shemdgom gadmoweristvis da pdf Akindzvistvis!
        radgan tl(transport-layer) iyo 2 erti da igive div tag classit tl
        amistvis calke tl klasistvis davwere patara funqcionali rata swored amokribos data
        pirveli da meore tl tagidan da tavebis tanmimdevroba ar dairgves.
    """
    print("Gethering All urls")
    sleep(0.2)
    ctr = 0  # for indexing purposes
    all_links = []
    for title in titles:
        if title == 'tl':
            sc = soup.find_all("div", class_='tl')[ctr]
            for second_tl in sc.find_all('a', href=re.compile("https://www.geeksforgeeks.org")):
                if 'href' in second_tl.attrs:

                    all_links.append(second_tl.attrs['href'])
            ctr += 1

        for i in soup.find("div", {"class": title}).find_all('a', href=re.compile("https://www.geeksforgeeks.org")):
            if 'href' in i.attrs and title != 'tl':

                all_links.append(i.attrs['href'])
    print(all_links)
    return all_links


def write_html(filename, head, title, body, mode='w'):
    "create html file and write all downloaded content"
    html = '.html'

    with open(filename+html, mode) as fp:
        fp.write(str(head))
        fp.write(str(title))
        fp.write(str(body))


def downloadPages(url_list):
    "Downloads Each page from url_list and merge them all??"
    links = url_list
    _breakpoint = "AP_G4GR_6"
    counter = 1
    for link in links:
        try:
            print("Downloading {}".format(link))
            soup = make_request(link)
            cont = soup.find_all('div', class_="entry-content")
            page_title = soup.h1
            page_body = str(cont[0])[0: str(cont[0]).find(_breakpoint)]
            page_head = soup.head
            style = make_style_tag(bsObj=soup, tagname=tagname, style=__style)
            page_head.append(style)

            write_html(filename=f"part {counter}",
                       head=page_head, title=page_title, body=page_body)
            counter += 1
        except:
            continue
    print("Done")


def main():
    "Call all functions"
    print(f"{bcolors.HEADER}Download is starting --------- {bcolors.ENDC}")
    url = 'https://www.geeksforgeeks.org/computer-network-tutorials'
    soup = make_request(url)
    titles = get_titles(soup)
    x = get_Links(titles, soup)

    main_thread = threading.Thread(target=downloadPages, args=[x])
    main_thread.start()
    print(f"{bcolors.OKGREEN}Download Finished Succesfully!")


main()
