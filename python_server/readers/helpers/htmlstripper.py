from __future__ import absolute_import

import re

def strip(data):
    p = re.compile(r'<.*?>|&nbsp;|&quot;')
    return p.sub('', data)
