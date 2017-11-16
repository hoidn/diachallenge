import requests

app_id = 'client_id'
app_secret = 'client_secret'
data = {'grant_type': 'client_credentials',
        'client_id': app_id,
        'client_secret': app_secret}
t = requests.post('https://api.yelp.com/oauth2/token', data=data)
access_token = t.json()['access_token']
