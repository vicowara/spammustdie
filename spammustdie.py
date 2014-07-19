#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import twitter
import argparse
from twitter_config import *

__THRESHOLD=100

def spammustdie(lang="ja",threshold=100):
    t=twitter.Twitter(auth=twitter.OAuth(ACCESS_KEY,ACCESS_SECRET,CONSUMER_KEY,CONSUMER_SECRET))
    search=t.search.tweets(q="goo.gl",lang=lang,count=100)
    blocked=[]
    for s in search["statuses"]:
        if("retweeted_status" in s):
            if(s["retweeted_status"]["retweet_count"]>threshold):
                t.blocks.create(screen_name=s["retweeted_status"]["user"]["screen_name"])
                blocked.append(s["retweeted_status"]["user"]["name"])
        else:
            if(s["retweet_count"]>threshold):
                t.blocks.create(screen_name=s["user"]["screen_name"])
                blocked.append(s["user"]["name"])
    print("{count} user has blocked.".format(count=len(blocked)))
    print("blocked user:\n",str(blocked))

def main():
    parser=argparse.ArgumentParser(description="report spam")
    parser.add_argument("-l","--lang",nargs="?",type=str)
    args=parser.parse_args()
    if(args.lang):
        spammustdie(lang=args.lang,threshold=__THRESHOLD)
    else:
        spammustdie(threshold=__THRESHOLD)

if __name__=="__main__":
    main()
