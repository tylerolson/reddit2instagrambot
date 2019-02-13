import praw
import json
import requests
import shutil
from InstagramAPI import InstagramAPI

foundSubs = []
doneSubs = []
subsToUpload = []

with open("config.json", "r") as configJSON:
     config = json.load(configJSON)
instaapi = InstagramAPI(config["instagram"]["username"], config["instagram"]["password"])
#instaapi.login()

def connectReddit():
    reddit = praw.Reddit(client_id=config["reddit"]["client_id"], client_secret=config["reddit"]["client_secret"], username=config["reddit"]["username"], password=config["reddit"]["password"], user_agent=config["reddit"]["user_agent"])
    sub_rl = reddit.subreddit('rocketleague')

    for submission in reddit.subreddit('RocketLeague').hot(limit=10):
        if (not submission.stickied):
            if (not submission.over_18):
                if ('.png' in submission.url):
                    print("Found PNG")
                    print(submission.title.encode("utf-8"))
                    print('\n')
                    foundSubs.append({"id": submission.id, "url": submission.url, "format": ".png", "title": submission.title, "author": submission.author.name})
                if ('.jpg' in submission.url):
                    print("Found JPG")
                    print(submission.title.encode("utf-8"))
                    print('\n')
                    foundSubs.append({"id": submission.id, "url": submission.url, "format": ".jpg", "title": submission.title, "author": submission.author.name})
                if ('v.redd' in submission.url):
                    print("Found MP4")
                    print(submission.title.encode("utf-8"))
                    print('\n')
                    foundSubs.append({"id": submission.id, "url": submission.media['reddit_video']['fallback_url'], "format": ".mp4", "title": submission.title, "author": submission.author.name})

    with open("done.json", "r") as doneFile:
        done = json.load(doneFile)
        for sub in foundSubs:
            if sub["id"] not in done:
                image_data = requests.get(sub["url"], stream=True)
                with open("media/" + sub["id"] + sub["format"], "wb") as handler:
                    shutil.copyfileobj(image_data.raw, handler)
                subsToUpload.append(sub)
                doneSubs.append(sub["id"])
                print("Downloaded " + sub["id"] + sub["format"])
                caption = sub["title"] + "\n-------------------------\nCredit: u/" + sub["author"] + "\n\n#rocketleague #rocketleagueclips #psyonix #reddit"
                #if sub["format"] is not ".mp4":
                    #instaapi.uploadPhoto("media/" + sub["id"] + sub["format"], caption)
                print("Uploaded to Instagram!")
            if sub["id"] in done:
                print("Already uploaded " + sub["id"])

    print(doneSubs)
    print(subsToUpload)

    done.extend(doneSubs)
    with open("done.json", "w") as doneFile:
        json.dump(done, doneFile)

connectReddit()
