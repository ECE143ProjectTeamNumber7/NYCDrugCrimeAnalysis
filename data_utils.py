import pandas as pd
import numpy as np

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