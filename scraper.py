import requests
import json
from bs4 import BeautifulSoup
import re


with open('token.json', 'r') as f:
    token = json.load(f)['access_token']
headers = {'Authorization': 'Bearer %s' % token}


url = 'https://api.yelp.com/v3/businesses/search'

def search_business(name):
    """
    Return url corresponding to Yelp page for the given the restaurant if
    a match is found. Otherwise raises a ValueError.
    """

    params = {
              'limit': 1,
              'term': name,
              'location': 'New York City'
             }

    resp = requests.get(url=url, params=params, headers=headers)
    import pprint
    result = resp.json()
    if not result:
        raise ValueError("No search results")
    match = result['businesses'][0]
    categories = match['categories'][0]
    if 'pizza' not in [v for v in categories.values()]\
            or match['name'].lower() != name.lower():
        raise ValueError("No matching search result")
    return match['url']

def scrape_reviews(full_url):
    """
    Return html of the given fully-qualified url.
    """
    from urllib import parse
    url = full_url.split('?')[0]
    pars = parse.parse_qs(parse.urlparse(url).query)
    pardict = {k: v[0] for k, v in pars.items()}
    resp = requests.get(url = url, headers = headers, params = pardict)
    return resp.text

def recent_reviews(url, n):
    txt = scrape_reviews(url)
    soup = BeautifulSoup(txt, 'html.parser') 
    reviews = soup.findAll('div',{'itemprop':re.compile("review")})[:n]
    return reviews

def review_score(review):
    elt = review.find('meta', {'itemprop': 'ratingValue'})
    return float(elt.attrs['content'])

#def validate_search_result(json_record):
#    """
#    Return true if search result is valid, false otherwise.
#    """
