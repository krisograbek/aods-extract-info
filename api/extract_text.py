import spacy
from spacy.matcher import Matcher

nlp = spacy.load('en_core_web_sm')


def get_sentences(lines):
    """" Returns sentences containing given keywords
    
    Parameters
    ----------
    lines : list(str)
        text from transcripts as a list of strings
    Returns
    -------
    sents : list(str)
        a list sentences containing keywords and capitalized words in it
    """

    txt = " ".join(lines)
    # convert text to Doc class from spaCy
    doc = nlp(txt)

    matcher = Matcher(nlp.vocab)
    sent_matcher = Matcher(nlp.vocab)

    # pattern to find keywords
    # NOTE: We use `lemma` in order to also find plural forms
    keyword_pattern = [{"LEMMA":  {"IN": ["book", "podcast", "website"]}}]
    
    matcher.add("book", [keyword_pattern])
    # return all the tokens containing defined keywords
    matches = matcher(doc)

    # pattern for capitalized words
    capitalized = [
        # find words that start with a capital letter, exclude sentence beginnings
        [{"IS_TITLE": True, "IS_SENT_START": False, "LENGTH": {">=": 2}}],
        # find all PERSON Named Entities
        [{"ENT_TYPE": "PERSON"}]]

    sent_matcher.add("person", capitalized)

    # initialize a list to store sentences
    sents = list()
    sent_ids = list()
    for match_id, start, end in matches:
        token = doc[start]
        # get the sentence for the found word
        sent = token.sent
        if (sent.start not in sent_ids):        # check if already in sentences
            # convert the sentence to Doc
            sent_doc = nlp(sent.text)
            # find Capitalized words in a sentence
            sent_matches = sent_matcher(sent_doc)
            if (len(sent_matches) > 0):         # if words found
                # add to sentences we return
                sents.append(sent.text)
                sent_ids.append(sent.start)

    print("Found ", len(sents))

    return sents
