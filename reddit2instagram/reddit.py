import getpass
import json
import logging
import praw
import requests
import shutil

logger = logging.getLogger("main")


def connect_reddit(config):
    """Return a Reddit connection using credentials specified"""
    if not config["reddit"]["password"]:
        config["reddit"]["password"] = getpass.getpass()

    reddit_conn = praw.Reddit(client_id=config["reddit"]["client_id"],
                              client_secret=config["reddit"]["client_secret"],
                              username=config["reddit"]["username"],
                              password=config["reddit"]["password"],
                              user_agent=config["reddit"]["user_agent"])

    return reddit_conn


def scrape_subreddit(reddit_conn, subreddit):
    found_subs = []
    for submission in reddit_conn.subreddit(subreddit).hot(limit=10):
        if (not submission.stickied):
            if (not submission.over_18):
                if ('.png' in submission.url):
                    logger.info("Found PNG ({0})".format(submission.title))
                    found_subs.append({"id": submission.id,
                                       "url": submission.url,
                                       "format": ".png",
                                       "title": submission.title,
                                       "author": submission.author.name})
                if ('.jpg' in submission.url):
                    logger.info("Found JPG ({0})".format(submission.title))
                    found_subs.append({"id": submission.id,
                                       "url": submission.url,
                                       "format": ".jpg",
                                       "title": submission.title,
                                       "author": submission.author.name})
                if ('v.redd' in submission.url):
                    logger.info("Found MP4 ({0})".format(submission.title))
                    found_subs.append({"id": submission.id,
                                       "url": submission.media['reddit_video']['fallback_url'],
                                       "format": ".mp4",
                                       "title": submission.title,
                                       "author": submission.author.name})

    return found_subs


def download_posts(found_posts, filename="done.json"):
    try:
        with open(filename, "r") as done_file:
            completed_ids = json.load(done_file)
    except FileNotFoundError:
        completed_ids = []

    for post in found_posts:
        if post["id"] not in completed_ids:
            logger.debug("Fetching data from {0}".format(post["url"]))
            image_data = requests.get(post["url"], stream=True)
            with open("media/" + post["id"] + post["format"], "wb") as handler:
                shutil.copyfileobj(image_data.raw, handler)

            # subsToUpload.append(post)
            completed_ids.append(post["id"])
            logger.debug("Downloaded {0}{1}".format(post["id"], post["format"]))
            # caption = post["title"] + "\n-------------------------\nCredit: u/" + post["author"] + "\n\n#rocketleague #rocketleagueclips #psyonix #reddit"
            #if sub["format"] is not ".mp4":
                #instaapi.uploadPhoto("media/" + sub["id"] + sub["format"], caption)
            logger.info("Uploaded {0}{1} to Instagram!".format(post["id"], post["format"]))
        else:
            logger.info("Already uploaded {0}{1}".format(post["id"], post["format"]))

    # print(subsToUpload)
    with open(filename, "w") as done_file:
        json.dump(completed_ids, done_file)
