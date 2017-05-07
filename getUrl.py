#!/usr/bin/python3
import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup
import shutil
import sys
import re
import os

if __name__ == "__main__":
    with urllib.request.urlopen('https://www.eclipse.org/downloads/eclipse-packages/?osType=linux&release=undefined') as f:
        page = BeautifulSoup(f.read(), 'html.parser')
        a = page.find(lambda tag: tag.name == "a" and tag.string is not None and tag.string.strip() == "Eclipse IDE for Java EE Developers")
        b64 = a.parent.parent.parent.find(lambda tag: tag.string is not None and tag.string.strip().lower() == '64 bit').find(**{'class':'downloadLink'})['href']
        b64 = 'https://www.eclipse.org' + b64
    with urllib.request.urlopen(b64) as f:
        page = BeautifulSoup(f.read(), 'html.parser')
        link = page.find(href = re.compile('^download\.php.+'))['href']
        link = 'https://www.eclipse.org/downloads/' + link
    with urllib.request.urlopen(link) as f:
        page = BeautifulSoup(f.read(), 'html.parser')
        finalLink = page.find(lambda tag: tag.name == "a" and tag.string is not None and tag.string.strip() == "click here")["href"]
        with urllib.request.urlopen(finalLink) as f, os.fdopen(sys.stdout.fileno(), 'wb') as stdout:
            shutil.copyfileobj(f, stdout)
