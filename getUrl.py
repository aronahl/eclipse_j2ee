#!/usr/bin/python3
import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup
import sys
import re
import os
import hashlib

if __name__ == "__main__":
    with urllib.request.urlopen('https://www.eclipse.org/downloads/eclipse-packages/?osType=linux&release=undefined') as f:
        page = BeautifulSoup(f.read(), 'html.parser')
        a = page.find(lambda tag: tag.name == "a" and tag.string is not None and tag.string.strip() == "Eclipse IDE for Enterprise Java Developers")
        b64 = a.parent.parent.parent.find(lambda tag: tag.name == "span" and tag["class"] == ["linux"]).find("a")["href"]
        b64 = 'https:' + b64
        print(b64)
    with urllib.request.urlopen(b64) as f:
        page = BeautifulSoup(f.read(), 'html.parser')
        finalLink = page.find(lambda tag: tag.name == "a" and tag.string is not None and tag.string.strip().lower() == "direct link to file")["href"]
        finalLink = 'https://www.eclipse.org/downloads/' + finalLink
        shaLink = finalLink.replace('download.php', 'sums.php')
    with urllib.request.urlopen(shaLink) as f:
        shasum = bytes.fromhex(f.read().split()[0].decode('utf-8'))
        #link = page.find(href = re.compile('^download\.php.+'))['href']
        #link = 'https://www.eclipse.org/downloads/' + link
    #with urllib.request.urlopen(link) as f:
    #    page = BeautifulSoup(f.read(), 'html.parser')
    #    finalLink = page.find(lambda tag: tag.name == "a" and tag.string is not None and tag.string.strip() == "click here")["href"]
    sha = hashlib.sha512()
    with urllib.request.urlopen(finalLink) as f, os.fdopen(sys.stdout.fileno(), 'wb') as stdout:
        for part in iter(lambda: f.read(8192), b""):
            sha.update(part)
            stdout.write(part)
        if sha.digest() != shasum:
            stdout.write('sha512 check failed'.encode('utf-8'))
            raise Exception('sha512 check failed')
