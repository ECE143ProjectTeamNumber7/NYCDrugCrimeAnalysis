import pandas as pd
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords

def group_count_parks(parks):
    nltk.download('punkt')
    all_text = ' '.join(parks.unique())

    locs = word_tokenize(all_text.lower())  # Convert to lowercase for case-insensitivity

    top_locs = FreqDist(locs).most_common(15)
    park_loc_count = parks.value_counts().to_dict()
    freq_loc_count = {word[0]: 0 for word in top_locs}

    for loc in park_loc_count:
        for freq_loc in freq_loc_count:
            if freq_loc in loc.lower():
                freq_loc_count[freq_loc] += park_loc_count[loc]

    freq_loc_count.pop("'s")
    freq_loc_count.pop('on')
    freq_loc_count.pop('st.')
    freq_loc_count.pop('avenue')
    freq_loc_count.pop('south')
    freq_loc_count.pop('street')

    return freq_loc_count

def count_keywords(column, keywords:list = {}):
    data_count = column.value_counts().to_dict()
    if len(keywords) == 0:
        return data_count

    key_count = dict(zip(keywords, [0] * len(keywords)))
    other_count = 0

    for data in data_count:
        for key in key_count:
            if key in data.lower():
                key_count[key] += data_count[data]
                break
        else:
            other_count += data_count[data]

    key_count['other'] = other_count

    return key_count