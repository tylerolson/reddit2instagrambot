import json
import logging
import os.path

logger = logging.getLogger("main")


def check_config(config_path="config.json"):
    if os.path.exists(config_path):
        logger.debug("Config file exists")
    else:
        logger.info("A config does not exist, please make one")
        with open(config_path, "w") as config_file:
            json.dump(create_config(), config_file)


def create_config():
    logger.info("Enter your Reddit client ID")
    client_id = input()
    logger.info("Enter your Reddit client secret")
    client_secret = input()
    logger.info("Enter your Reddit username")
    reddit_username = input()
    logger.info("Enter your Instagram username")
    instagram_username = input()

    return {
      "reddit": {
          "client_id": client_id,
          "client_secret": client_secret,
          "username": reddit_username
      },
      "instagram": {
        "username": instagram_username
      }
    }
