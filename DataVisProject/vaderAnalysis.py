import json

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import numpy as np

nltk.download('vader_lexicon')

pointMachine = SentimentIntensityAnalyzer()
def sentiment_analyzer_scores(x):
    score = pointMachine.polarity_scores(x)
    return score


def create_dataframe():
    my_dataframe = pd.read_json('data/results.json', orient='records')
    my_dataframe['sentiment'] = my_dataframe['tweet'].apply(lambda x: 'NaN' if pd.isnull(x) else sentiment_analyzer_scores(x))
    my_dataframe['num'] = my_dataframe['sentiment'].apply(lambda score_dict: score_dict['compound'])
    my_dataframe['num_results'] = my_dataframe['num'].apply(
        lambda c: 'positive' if c > 0.05 else ('negative' if c < -0.05 else 'neutral'))
    process_json = my_dataframe.to_json(orient='index')
    parsed = json.loads(process_json)
    parsed = json.dumps(parsed)
    return parsed