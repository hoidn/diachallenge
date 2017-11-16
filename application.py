import numpy as np
import scraper
from functools import reduce

from flask import Flask, jsonify, render_template, request
app = Flask(__name__)

def process_query(name, n):
    """
    return (reviews, score) where reviews is a list of n reviews and
    score is the mean score over those reviews.

    Raises a ValueError if no business matching the provided name is found.
    """
    print('process query')
    print (name)
    print (n)
    url = scraper.search_business(name)
    print(url)
    reviews = scraper.recent_reviews(url, n)
    score = np.mean(list(map(scraper.review_score, reviews)))
    reviews = [record.text for record in scraper.recent_reviews(url, n)]
    reviews = '\n'.join(list(filter(lambda x: not x.isspace(), reviews)))
    #reviews = list(reduce(lambda a, b: a + b, map(lambda review: review.split('\n'),\
        #reviews)))
    return reviews, score

@app.route('/_query_restaurant')
def query_restaurant():
    name = request.args.get('name', 0, type=str)
    n = request.args.get('n', 0, type = int)
    try:
        reviews, score = process_query(name, n * 2)
        #print (reviews)
        print (score)
        return jsonify(reviews = reviews, score = str(round(score, 2)))
    except ValueError:
        return jsonify(reviews = '%s: not found' % name, score = '')


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 80)

