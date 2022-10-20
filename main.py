import config
import tweepy
from dotenv import load_dotenv
import os
import requests
import time

#twitter
AK  = config.API_KEY
AKS = config.API_KEY_SECRET
AT  = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET
auth = tweepy.OAuthHandler(AK, AKS)
auth.set_access_token(AT, ATS)
api = tweepy.API(auth, wait_on_rate_limit=True)

#slack
load_dotenv()
TOKEN = str(os.environ.get("SLACK_BOT_TOKEN"))
url = "https://slack.com/api/chat.postMessage"
headers = {"Authorization": "Bearer "+TOKEN}

def post_message(post_text):
    data = {
        'channel': "walnuts-健康な食事",
        'text': post_text
    }

    r = requests.post(url, headers=headers, data=data)
    print("return ", r.json())


with open('last_id.txt', 'r') as f:
    last_id=int(f.read())
while True:
    tweets_ps=[]
    for tweets in api.search_tweets(q="ごはん OR ご飯 from:walnuts1018",since_id=last_id+1,result_type="recent"):
        tweets_ps.insert(0,tweets.id)
        print(tweets)
    for i in tweets_ps:
        post_message("https://twitter.com/walnuts1018/status/"+str(tweets.id))

    if tweets_ps!=[]:
        with open('last_id.txt', 'w') as f:
            f.write(str(tweets_ps[-1]))
    time.sleep(5*60)

