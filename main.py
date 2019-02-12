import praw
import urllib
from InstagramAPI import InstagramAPI

subsToUpload = []

def connectReddit():
    reddit = praw.Reddit(client_id='info', client_secret='info', username='info', password='info', user_agent='xd')
    sub_rl = reddit.subreddit('rocketleague')

    for submission in reddit.subreddit('RocketLeague').hot(limit=10):
        if (not submission.stickied):
            if (not submission.over_18):
                if ('.png' in submission.url):
                    print(submission.title.encode("utf-8"))
                    print('Downloading...')
                    urllib.request.urlretrieve(submission.url, "media/" + submission.id + ".png")
                    print('Downloaded to ' + submission.id)
                    print('\n')
                    subsToUpload.append()
                if ('.jpg' in submission.url):
                    print(submission.title.encode("utf-8"))
                    print('Downloading...')
                    urllib.request.urlretrieve(submission.url, "media/" + submission.id + ".jpg")
                    print('Downloaded to ' + submission.id)
                    print('\n')
                if ('v.redd' in submission.url):
                    print(submission.title.encode("utf-8"))
                    print('Downloading...')
                    urllib.request.urlretrieve(submission.media['reddit_video']['fallback_url'], "media/" + submission.id + ".mp4")
                    print('Downloaded to ' + submission.id)
                    print('\n')

def connectInstagram():
    api = InstagramAPI("***REMOVED***", "***REMOVED***")
    api.login()

    path = 'test.jpg'
    caption = "Test"
    #api.uploadPhoto(path, caption)

#connectInstagram()
connectReddit()
