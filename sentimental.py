import json
import pandas as pd


# load custom sentimental dictionary
with open('data/dictionary/custom_dict.json') as f:
    js = json.loads(f.read())
custom_dict = pd.DataFrame(js)


# calculate sentimental score
def get_senti_score(review):
    score = 0
    for keyword in review:
        for word, pol in custom_dict.values:
            if keyword == word:
                score += pol
                break
    return score