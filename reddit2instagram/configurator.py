import json
import os
import getpass
from cryptography.fernet import Fernet
from common import *


def check_config(config_path=os.path.join(BASE_DIR, "config.json")):
    if os.path.exists(config_path):
        logger.debug("Config file exists")
    else:
        logger.info("A config does not exist, please make one")
        with open(config_path, "w") as config_file:
            json.dump(create_config(), config_file, indent=4)


def get_config(config_path=os.path.join(BASE_DIR, "config.json")):
    check_config()
    with open(config_path, "r") as config_json:
        config = json.load(config_json)

    return config


def encrypt_password(key, password):
    cipher_suite = Fernet(key)
    password_encrypted = cipher_suite.encrypt(password)
    return password_encrypted


def decrypt_password(key, password_encrypted):
    cipher_suite = Fernet(key)
    password_decoded = cipher_suite.decrypt(password_encrypted)
    return password_decoded


def create_config():
    configuration = { "encrypt_key": Fernet.generate_key().decode("UTF-8"),
                      "reddit": {},
                      "instagram": {}
                    }

    configuration["reddit"]["client_id"] = input("Enter your Reddit client ID: ")
    configuration["reddit"]["client_secret"] = input("Enter your Reddit client secret: ")
    configuration["reddit"]["username"] = input("Enter your Reddit username: ")
    password = getpass.getpass("Enter your Reddit password: ")
    configuration["reddit"]["password"] = encrypt_password(configuration["encrypt_key"], password.encode("UTF-8")).decode("UTF-8")

    configuration["instagram"]["username"] = input("Enter your Instagram username: ")
    password = getpass.getpass("Enter your Instagram password: ")
    configuration["instagram"]["password"] = encrypt_password(configuration["encrypt_key"], password.encode("UTF-8")).decode("UTF-8")
    configuration["instagram"]["tags"] = input("Enter Instagram tags: ")

    return configuration
