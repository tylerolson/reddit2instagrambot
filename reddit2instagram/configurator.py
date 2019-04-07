import json
import logging
import os
import getpass
from cryptography.fernet import Fernet

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logger = logging.getLogger("main")


def check_config(config_path=os.path.join(BASE_DIR, "config.json")):

    if os.path.exists(config_path):
        logger.debug("Config file exists")
    else:
        logger.info("A config does not exist, please make one")
        with open(config_path, "w") as config_file:
            json.dump(create_config(), config_file, indent=4)


def encrypt_password(key, password):
    cipher_suite = Fernet(key)
    password_encrypted = cipher_suite.encrypt(password)
    return password_encrypted


def decrypt_password(key, password_encrypted):
    cipher_suite = Fernet(key)
    password_decoded = cipher_suite.decrypt(password_encrypted)
    return password_decoded


def create_config():
    encrypt_key = Fernet.generate_key()

    logger.info("Enter your Reddit client ID")
    client_id = input()
    logger.info("Enter your Reddit client secret")
    client_secret = input()
    logger.info("Enter your Reddit username")
    reddit_username = input()
    logger.info("Enter your Reddit password")
    reddit_password = getpass.getpass()
    logger.info("Enter your Instagram username")
    instagram_username = input()
    logger.info("Enter your Instagram password")
    instagram_password = getpass.getpass()
    logger.info("Enter Instagram tags")
    instagram_tags = input()

    reddit_password_encrypted = encrypt_password(encrypt_key, reddit_password.encode('UTF-8'))
    instagram_password_encrypted = encrypt_password(encrypt_key, instagram_password.encode('UTF-8'))

    return {
        "encrypt_key": encrypt_key.decode('UTF-8'),
        "reddit": {
            "client_id": client_id,
            "client_secret": client_secret,
            "username": reddit_username,
            "password": reddit_password_encrypted.decode('UTF-8')
        },
        "instagram": {
            "username": instagram_username,
            "password": instagram_password_encrypted.decode('UTF-8'),
            "tags": instagram_tags
        }
    }
