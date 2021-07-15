import datetime as dt
from flask import Flask
from extract_text import (
    get_info, 
    get_sentences,
    get_transcripts
)

app = Flask(__name__)


batch_size = 50

@app.route('/text')
def get_extracted_sentences():
    scripts = get_transcripts()
    infos = list()
    for script in scripts:
        # before = dt.datetime.now()
        # print("len lines:", len(script["text"]))
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

@app.route('/info')
def get_text_info():
    infos = get_info()
    print(infos)
    return {'infos': infos}
