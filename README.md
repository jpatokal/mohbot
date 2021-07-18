# mohbot
Scrape reddit for Singapore Ministry of Health (MOH) updates posted to Reddit

## Install

```
virtualenv env
. env/bin/activate
pip3 install requests pandas pyyaml
cp config.yaml.example config.yaml
```

Obtain a client ID and secret using the [instructions here](https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c),
then plug them into your `config.yaml`.

```
python3 mohbot.py
```

## Sample output with Google Sheets visualization

[MOH publication time vs cases correlation](https://docs.google.com/spreadsheets/d/1ZgQORBMLDMcYwZUu9ompHkJ_W3rRe8VPOyR47_bz2BQ/edit#gid=1834309100)

## Credits

Code heavily borrowed from [How to Use the Reddit API in Python](https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c).
