import json
import imageio
import os
from InstagramAPI import InstagramAPI
from reddit2instagram import configurator
from common import *

imageio.plugins.ffmpeg.download()


def upload_subs(found_subs, filename=os.path.join(BASE_DIR, "done.json")):
    try:
        with open(filename, "r") as done_file:
            uploaded_subs = json.load(done_file)
    except FileNotFoundError:
        uploaded_subs = []

    config = configurator.get_config()
    instagram_password_decrypted = configurator.decrypt_password(config["encrypt_key"], config["instagram"]["password"].encode('UTF-8'))
    instagram_password_decrypted_decoded = instagram_password_decrypted.decode('UTF-8')
    instagram_api = InstagramAPI(config["instagram"]["username"], instagram_password_decrypted_decoded)
    instagram_api.login()

    for sub in found_subs:
        sub_caption = "{0}\n\nCredit: u/{1} {2}\n\n{3}".format(sub["title"], sub["author"], sub["shortlink"], config["instagram"]["tags"])

        if sub["id"] not in uploaded_subs:
            if sub["format"] not in ".mp4":
                instagram_api.uploadPhoto(os.path.join(BASE_DIR, "media", sub["id"] + "_resized" + sub["format"]), caption=sub_caption)
                uploaded_subs.append(sub["id"])
                logger.info("Uploaded photo {0}{1} to Instagram!".format(sub["id"], sub["format"]))
            else:
                instagram_api.uploadVideo(os.path.join(BASE_DIR, "media", sub["id"] + sub["format"]), os.path.join(BASE_DIR, "media", sub["id"] + "_thumbnail.png"), caption=sub_caption)
                uploaded_subs.append(sub["id"])
                logger.info("Uploaded video {0}{1} to Instagram!".format(sub["id"], sub["format"]))
        else:
            logger.info("Already uploaded {0}{1}".format(sub["id"], sub["format"]))

    with open(filename, "w") as done_file:
        json.dump(uploaded_subs, done_file)
