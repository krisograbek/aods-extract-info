import time
from flask import Flask
from extract_text import get_info, get_checkouts

app = Flask(__name__)


@app.route('/text')
def get_text_beginning():
    sents = get_checkouts()
    print(sents)
    return {'text': sents}

@app.route('/info')
def get_text_info():
    infos = get_info()
    print(infos)
    return {'infos': infos}
