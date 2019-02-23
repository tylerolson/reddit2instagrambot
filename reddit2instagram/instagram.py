import getpass
import json
import logging
import subprocess
import imageio
from InstagramAPI import InstagramAPI

logger = logging.getLogger("main")
imageio.plugins.ffmpeg.download()


def upload_subs(found_subs, filename="done.json"):
    try:
        with open(filename, "r") as done_file:
            uploaded_subs = json.load(done_file)
    except FileNotFoundError:
        uploaded_subs = []

    with open("config.json", "r") as config_file:
        config_json = json.load(config_file)

    logger.info("Enter your Instagram password")
    instagram_password = getpass.getpass()
    instagram_api = InstagramAPI(config_json["instagram"]["username"], instagram_password)
    instagram_api.login();

    for sub in found_subs:
        sub_caption = sub["title"] + "\n-------------------------\nCredit: u/" + sub["author"] + "\n\n#rocketleague #rocketleagueclips #psyonix #reddit"

        if sub["id"] not in uploaded_subs:
            if sub["format"] not in ".mp4":
                subprocess.check_call(["instapy.exe", "-u", "***REMOVED***", "-p", "***REMOVED***", "-f", "media/" + sub["id"] + sub["format"], "-t", sub_caption])
                uploaded_subs.append(sub["id"])
                logger.info("Uploaded {0}{1} to Instagram!".format(sub["id"], sub["format"]))
            else:
                instagram_api.uploadVideo("media/" + sub["id"] + sub["format"], "media/thumbnail_" + sub["id"] + ".png", caption=sub_caption)
                uploaded_subs.append(sub["id"])
                logger.info("Uploaded {0}{1} to Instagram!".format(sub["id"], sub["format"]))
        else:
            logger.info("Already uploaded {0}{1}".format(sub["id"], sub["format"]))

    with open(filename, "w") as done_file:
        json.dump(uploaded_subs, done_file)
