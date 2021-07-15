import datetime as dt
from flask import Flask
from extract_text import (
    get_sentences
)
from helpers import get_transcripts

app = Flask(__name__)


batch_size = 50

@app.route('/text')
def get_extracted_sentences():
    scripts = get_transcripts()
    infos = list()
    for script in scripts:
        # before = dt.datetime.now()
        idx = 0
        sents = list()
        while idx < len(script["text"]):
            sents.extend(get_sentences(script["text"][idx: idx+batch_size]))
            idx = idx + batch_size
        info = {
            "title": script["title"],
            "sents": sents
        }
        infos.append(info)
        # print(dt.datetime.now() - before)
    return {'text': infos}
