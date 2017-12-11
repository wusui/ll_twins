#!/usr/bin/python
"""
Html Reader
"""

from urllib2 import urlopen
from contextlib import closing

def reader(html_page):
    """
    Simple html page reader.
    """
    with closing(urlopen(html_page)) as rfile:
        encoding = rfile.headers.getparam('charset')
        rtext = rfile.read()
    return unicode(rtext, encoding).encode('utf-8')

if __name__ == "__main__":
    info = reader(u"https://learnedleague.com/match.php?75&7&B_Pacific")
    print info
