from __future__ import absolute_import

from framework.celery import app
from visiter import visit

@app.task
def visit_page(url):
    return visit(url)
