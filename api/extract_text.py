import spacy
from spacy.matcher import Matcher

nlp = spacy.load('en_core_web_sm')


def get_lines(fpath):
    with open(fpath) as f:
        txt = f.readlines()
    
    return txt

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

def get_checkouts():
    lines = get_lines('../data/transcripts.txt')
    txt = " ".join(lines)
    doc = nlp(txt[50000:100000])

    matcher = Matcher(nlp.vocab)
    # Add match ID "HelloWorld" with no callback and one pattern
    pattern = [{"LOWER": "check"}, {"LOWER": "out"}]
    matcher.add("checkout", [pattern])
    matches = matcher(doc)

    sents = list()
    for match_id, start, end in matches:
        # print(match_id)
        token = doc[start]
        sent = token.sent.text
        sents.append(sent)

    print("Found ", len(sents))
    # print(sents)

    return sents
