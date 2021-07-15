import os
import re
import string

TRANS_DIR = '../data/transcripts/'


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


def get_transcripts():
    """
    Returns
    -------
    scripts : list(title: str, text: str)
        a list dictionaries containing the filename and it's content
    """
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

############## For Future Use  #################

# def remove_stopwords(tokens):
#     return [word for word in tokens if word not in stopwords]

# def remove_punctuations(tokens):
#     return [word for word in tokens if word not in string.punctuation]

# def clean_tokens(tokens):
#     tokens = remove_stopwords(tokens)
#     tokens = remove_punctuations(tokens)
#     return tokens
