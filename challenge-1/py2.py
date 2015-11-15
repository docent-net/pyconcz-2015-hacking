#!/usr/bin/python2
# -*- coding: utf-8 -*-
import formatter
import htmllib
import md5
import subprocess
import sys
import urllib


print 'Enter site URL to fetch:'
url = raw_input()

try:
    u = urllib.urlopen(url)
except IOError, e:
    print >> sys.stderr, 'Error: %s' % e
    exit(1)

parser = htmllib.HTMLParser(formatter.AbstractFormatter(formatter.NullWriter()))
html = u.read()
parser.feed(html)
print
print 'Title: %s' % parser.title
print

proc = subprocess.Popen(['md5sum'], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
out, _ = proc.communicate(html)
md5sum = out.split()[0]
print 'md5sum by Shell:  %s' % md5sum


m = md5.new()
m.update(html)
hexdigest = m.hexdigest()
print 'md5sum by Python: %s' % hexdigest


print
print
if md5sum == hexdigest:
    print 'They MATCH!'
    exit(0)
else:
    print >> sys.stderr, 'They don\'t MATCH!'
    exit(1)
