import requests
import pandas as pd
import yaml
from yaml.loader import SafeLoader
from datetime import datetime

# we use this function to convert responses to dataframes
def df_from_response(res):
    # initialize temp dataframe for batch of data in response
    df = pd.DataFrame()

    # loop through each post pulled from res and append to df
    for post in res.json()['data']['children']:
        df = df.append({
            'subreddit': post['data']['subreddit'],
            'title': post['data']['title'],
            'selftext': post['data']['selftext'],
            'upvote_ratio': post['data']['upvote_ratio'],
            'ups': post['data']['ups'],
            'downs': post['data']['downs'],
            'score': post['data']['score'],
            'link_flair_css_class': post['data']['link_flair_css_class'],
            'created_utc': datetime.fromtimestamp(post['data']['created_utc']).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'url': post['data']['url'],
            'id': post['data']['id'],
            'kind': post['kind']
        }, ignore_index=True)

    return df

with open('config.yaml') as f:
    config = yaml.load(f, Loader=SafeLoader)

# authenticate API
client_auth = requests.auth.HTTPBasicAuth(config['clientid'], config['secret'])
data = {
    'grant_type': 'password',
    'username': config['username'],
    'password': config['password']
}
headers = {'User-Agent': 'myBot/0.0.1'}

# send authentication request for OAuth token
res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=client_auth, data=data, headers=headers)
# extract token from response and format correctly
token = f"bearer {res.json()['access_token']}"
# update API headers with authorization (bearer token)
headers = {**headers, **{'Authorization': token}}

# initialize dataframe and parameters for pulling data in loop
data = pd.DataFrame()
params = {'limit': 100, 'q': 'local cases', 'restrict_sr': True}

# make request
res = requests.get("https://oauth.reddit.com/r/singapore/search",
                   headers=headers,
                   params=params)
df = df_from_response(res)

df['cases'] = df['title'].str.split(' ', expand=True)[0]
dt = pd.to_datetime(df['created_utc']).dt
df['hour'] = dt.hour
df['minutes'] = (dt.hour * 60 + dt.minute) - 900 # 3 PM

# drop rows that are not pointing to MOH or not posted at afternoon update time
df.drop(df[~df['url'].str.contains('moh.gov.sg')]['url'].index, inplace=True)
df.drop(df[df['hour'] < 15].index, inplace=True)
df.drop(df[df['hour'] >= 22].index, inplace=True)

print(df.to_csv(columns=['cases', 'minutes', 'title','created_utc']))
