import os
import re
import spacy
from spacy.matcher import Matcher

nlp = spacy.load('en_core_web_sm')


TRANS_DIR = '../data/transcripts/'

def remove_stopwords(tokens):
    return [word for word in tokens if word not in stopwords]

def remove_punctuations(tokens):
    return [word for word in tokens if word not in string.punctuation]

def clean_tokens(tokens):
    tokens = remove_stopwords(tokens)
    tokens = remove_punctuations(tokens)
    return tokens

def remove_timestamps(lines):
    """
    removes beginnings, e.g. Speaker4: [00:45:09] 
    or just timestamps, e.g. [00:49:54]
    """
    clean = list()

    for line in lines:
        if line == "\n":
            continue
        if line.startswith(r'Speaker'):
            line = re.sub(r'Speaker\d:', "", line)
        line = re.sub(r'\[\d\d:\d\d:\d\d\]', "", line)
        clean.append(line)
    return clean

def get_lines(fpath):
    with open(fpath) as f:
        txt = f.readlines()
    
    return txt

def get_transcripts():
    scripts = list()
    for script in os.listdir(TRANS_DIR):
        with open(os.path.join(TRANS_DIR, script)) as f:
            txt = f.readlines()
            # remove garbage
            txt = remove_timestamps(txt)
            scripts.append({
                "title": script,
                "text": txt
            })
    return scripts

def get_first_n_docs(n: int):
    lines = get_lines('../data/transcripts.txt')
    return lines[:n]

def get_info():
    lines = get_lines('../data/transcripts.txt')
    txt = " ".join(lines)
    doc = nlp(txt[:100])

    # print(list(doc)[:5])

    infos = list()
    for token in doc:
        info = {
            "text": token.text,
            "pos": token.pos_,
            "dep": token.dep_
        }
        infos.append(info)

    print("getting infos")

    return infos

def get_sentences(lines):
    # lines = get_lines('../data/transcripts.txt')
    txt = " ".join(lines)
    # print("txt len: ", len(txt))
    doc = nlp(txt)

    matcher = Matcher(nlp.vocab)
    sent_matcher = Matcher(nlp.vocab)
    # Add match ID "HelloWorld" with no callback and one pattern
    # pattern = [{"LOWER": "check"}, {"LOWER": "out"}]
    book_pattern = [{"LEMMA": "book"}]
    podcast_pattern = [{"LEMMA": "podcast"}]
    website_pattern = [{"LEMMA": "website"}]
    matcher.add("book", [book_pattern])
    matcher.add("podcast", [podcast_pattern])
    # matcher.add("course", [course_pattern])
    matcher.add("website", [website_pattern])
    matches = matcher(doc)

    person_pattern = [{"ENT_TYPE": "PERSON"}]
    person_pattern = [
        [{"IS_TITLE": True, "IS_SENT_START": False, "LENGTH": {">=": 3}}],
        [{"ENT_TYPE": "PERSON"}]]
    sent_matcher.add("person", person_pattern)

    sents = list()
    sent_ids = []
    for match_id, start, end in matches:
        token = doc[start]
        sent = token.sent

        sent_doc = nlp(sent.text)
        sent_matches = sent_matcher(sent_doc)
        # print("sent matches", len(sent_matches))
        if (sent.start not in sent_ids) and (len(sent_matches) > 0):
            sents.append(sent.text)
            sent_ids.append(sent.start)
            # print([sent_doc[st] for _, st, _ in sent_matches])

    print("Found ", len(sents))
    # print(sents)

    return sents
