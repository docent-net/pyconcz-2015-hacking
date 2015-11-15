#!/usr/bin/python2
# -*- coding: utf-8 -*-
from __future__ import print_function
from builtins import input
import formatter
from html.parser import HTMLParser
import hashlib
import subprocess
import sys
from urllib.request import urlopen

print('Enter site URL to fetch:')
#url = input()
url = 'http://maciej.lasyk.info'

try:
    u = urlopen(url)
except IOError as e:
    print('Error: %s' % e, file=sys.stderr)
    exit(1)

inTitle = False

class ExtendedHTMLParser(HTMLParser):
    title = False
    def handle_starttag(self, tag, attrs):
        global inTitle
        if tag.upper() == "title":
            inTitle = True
    def handle_endtag(self, tag):
        global inTitle
        if tag.upper() == "title":
            inTitle = False
    def handle_data(self, data):
        global inTitle
        if inTitle:
            self.title = data

parser = ExtendedHTMLParser(formatter.AbstractFormatter(formatter.NullWriter()))
html = u.read().decode(u.headers.get_content_charset('utf8'))
parser.feed(html)


print("\nTitle: %s\n" % parser.title)

proc = subprocess.Popen(['md5sum'], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
out, _ = proc.communicate(bytes(html, 'UTF-8'))
md5sum = out.split()[0]
print('md5sum by Shell:  %s' % md5sum)


m = hashlib.md5()
m.update(bytes(html,'UTF-8'))
hexdigest = m.hexdigest()
print('md5sum by Python: %s' % hexdigest)

if md5sum == hexdigest:
    print("\n\nThey MATCH!")
    exit(0)
else:
    print('They don\'t MATCH!', file=sys.stderr)
    exit(1)
