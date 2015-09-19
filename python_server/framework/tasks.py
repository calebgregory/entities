from __future__ import absolute_import

from framework.celery import app
import nltk

@app.task
def tokenize(message):
    tokens = nltk.word_tokenize(message)
    return tokens
