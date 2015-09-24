from __future__ import absolute_import

import time
import urllib2
from urllib2 import urlopen
import re
import cookielib
from cookielib import CookieJar
import datetime
import json

from helpers import htmlstripper as hs

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-Agent', 'Mozilla/5.0')]

def visit(url):
    try:
        page = url;
        sourceCode = opener.open(page).read()
        headline = re.findall(r'<h1.*?>(.*?)</h1', str(sourceCode))
        if 'cnn' in page:
            linesOfInterest = re.findall(r'<p class="zn-body__paragraph">(.*?)</p>', str(sourceCode))
        elif 'nytimes' in page:
            linesOfInterest = re.findall(r'<p class="story-body-text.*?itemprop="articleBody".*?>(.*?)</p>', str(sourceCode))
        else:
            linesOfInterest = re.findall(r'<p>(.*?)</p>', str(sourceCode))
        output = {}
        output['headline'] = headline[0]
        content = []
        for line in linesOfInterest:
            content.append(hs.strip(line))
        output['content'] = content
        return json.dumps(output)
    except Exception, e:
        print str(e)
