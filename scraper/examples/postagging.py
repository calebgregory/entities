'''
CC      coordinating conjection
CD      cardinal digit
DT      determiner
EX      existential there (i.e., "there is" or "there exists")
FW      foreign word
IN      preposition/subordinating conjunction
JJ      adjective               'big'
JJR     adjective, comparative  'bigger'
JJS     adjective, superlative  'biggest'
LS      list marker             1)
MD      modal                   'could', 'would'
NN      noun, singular
NNS     noun, plural
NNP     proper noun, singular
NNPS    proper noun, plural
PDT     predeterminer           'all the things'
POS     possessive ending       "parent's"
PRP     personal pronoun        'I', 'you', 'he'
PRPS    possessive pronoun      'my', 'your', 'his'
RB      adverb                  'very'
RBR     abverb, comparative     'better'
RBS     adverb, superlative     'best'
RP      particle                'give up'
TO      to                      go 'to' the store
UH      interjection            'uhh'
VB      verb, base form         'take'
VBD     verb, past tense        'took'
VBG     verb, gerund/present participle     'taking'
VBN     verb, past participle   'taken'
VBP     verb, sing. present, non-3d         'take'
VBZ     verb, 3rd person sing. present      'takes'
WDT     wh-determiner           'which'
WP      wh-pronoun              'who', 'what'
WPS     possessive wh-pronoun   'whose'
WRB     wh-adverb               'where', 'when'
'''

import nltk
import re
import time

exampleArray = ['The incredibly intimidating NLP scares people away who are sissies.']

def processLanguage():
    try:
        for item in exampleArray:
            tokens = nltk.word_tokenize(item)
            tagged = nltk.pos_tag(tokens)

            namedEnt = nltk.ne_chunk(tagged, binary=True)
            print namedEnt

            time.sleep(1)
    except Exception, e:
        print str(e)

processLanguage()
