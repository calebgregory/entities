from __future__ import absolute_import

from framework.celery import app

import time
import urllib2
from urllib2 import urlopen
import re
import cookielib
from cookielib import CookieJar
import datetime
import json

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-Agent', 'Mozilla/5.0')]

def strip(data):
    data = re.sub(r'&quot;','"',data)
    data = re.sub(r'&amp;','&',data)
    p = re.compile(r'<.*?>|&nbsp;')
    return p.sub('', data)

@app.task
def visit(url, sentiment_value):
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
            content.append(strip(line))
        output['content'] = content
        output['url'] = url
        output['sentimentValue'] = sentiment_value
        return json.dumps(output)
    except Exception, e:
        print str(e)
