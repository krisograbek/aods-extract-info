import spacy
from spacy.matcher import Matcher
from helpers import get_lines


nlp = spacy.load('en_core_web_sm')


def get_info():
    lines = get_lines('../data/transcripts.txt')
    txt = " ".join(lines)
    doc = nlp(txt[:100])

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
