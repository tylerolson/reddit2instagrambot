import getpass
import json
import logging
import praw
import requests
import shutil
from PIL import Image
from reddit2instagram import configurator, image_utils

logger = logging.getLogger("main")


def connect_reddit():
    configurator.check_config()
    logger.info("Enter your Reddit password")
    reddit_password = getpass.getpass()

    with open("config.json", "r") as config_file:
        config_json = json.load(config_file)

    reddit_conn = praw.Reddit(client_id=config_json["reddit"]["client_id"],
                              client_secret=config_json["reddit"]["client_secret"],
                              username=config_json["reddit"]["username"],
                              password=reddit_password,
                              user_agent="reddit2instagram")

    return reddit_conn


def scrape_subreddit(reddit_conn, subreddit):
    found_subs = []
    for submission in reddit_conn.subreddit(subreddit).hot(limit=15):
        if not submission.stickied:
            if not submission.over_18:
                if '.png' in submission.url:
                    logger.info("Found PNG ({0})".format(submission.title))
                    found_subs.append({"id": submission.id,
                                       "url": submission.url,
                                       "format": ".jpeg",
                                       "title": submission.title,
                                       "author": submission.author.name})
                if '.jpg' in submission.url:
                    logger.info("Found JPG ({0})".format(submission.title))
                    found_subs.append({"id": submission.id,
                                       "url": submission.url,
                                       "format": ".jpg",
                                       "title": submission.title,
                                       "author": submission.author.name})
                if 'v.redd' in submission.url:
                    logger.info("Found MP4 ({0})".format(submission.title))
                    logger.debug("Found thumbnail {0}".format(submission.preview["images"][0]["source"]["url"]))
                    found_subs.append({"id": submission.id,
                                       "url": submission.media['reddit_video']['fallback_url'],
                                       "url_thumbnail": submission.preview["images"][0]["source"]["url"],
                                       "format": ".mp4",
                                       "title": submission.title,
                                       "author": submission.author.name})

    return found_subs


def download_subs(found_subs, filename="done.json"):
    try:
        with open(filename, "r") as done_file:
            uploaded_subs = json.load(done_file)
    except FileNotFoundError:
        uploaded_subs = []

    for sub in found_subs:
        if sub["id"] not in uploaded_subs:
            logger.debug("Fetching data from {0}".format(sub["url"]))

            image_data = requests.get(sub["url"], stream=True)
            with open("media/" + sub["id"] + sub["format"], "wb") as handler:
                shutil.copyfileobj(image_data.raw, handler)
            logger.debug("Downloaded image {0}{1}".format(sub["id"], sub["format"]))

            if sub["format"] in '.mp4':
                logger.debug("Downloading video thumbnail")
                thumbnail_data = requests.get(sub["url_thumbnail"], stream=True)
                with open("media/" + sub["id"] + "_thumbnail.png", "wb") as handler_thumbnail:
                    shutil.copyfileobj(thumbnail_data.raw, handler_thumbnail)
                logger.debug("Downloaded video {0}{1}".format(sub["id"], sub["format"]))
            else:
                image_open = Image.open("media/" + sub["id"] + sub["format"])
                image_utils.image_to_square(image_open, "media/" + sub["id"] + "_resized" + sub["format"])
                logger.debug("Resized image to {0}".format("media/" + sub["id"] + "_resized" + sub["format"]))
        else:
            logger.debug("Already uploaded {0}{1}".format(sub["id"], sub["format"]))
