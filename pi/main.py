# coding: UTF-8
import logging
from gassist import gassist

if __name__ == '__main__':
    # Setup logging.
    logging.basicConfig(level=logging.INFO)

    text_query='ぴよログにおしっこの記録を頼みたい'
    text_query='ぴよログにうんちの記録を頼みたい'
    text_query='ぴよログに寝たことの記録を頼みたい'
    text_query='ぴよログに起きたことの記録を頼みたい'
    gassist(text_query)
