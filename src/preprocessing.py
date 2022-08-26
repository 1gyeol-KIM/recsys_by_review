import re
from konlpy.tag import Mecab

def clean_text(text):
    review_removed = re.sub('[^가-힣 ]', '', text)
    return review_removed


def get_nouns(tokenizer, sentence):
    tagged = tokenizer.pos(sentence)
    nouns = [s for s, t in tagged if t in ['NNG', 'NNP', 'VA', 'XR'] and len(s) > 1]
    return nouns


def tokenize(review):
    tokenizer = Mecab()
    processed_data = []
    for sent in review:
        sentence = clean_text(sent)
        processed_data.append(get_nouns(tokenizer, sentence))
    return processed_data


