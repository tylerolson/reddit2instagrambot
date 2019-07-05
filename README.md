# reddit2instagrambot

Python script/bot to automatically download top submissions from desired Subreddit and upload them to Instagram.

## Getting Started

There are two easy ways to use the script.

1. Clone project then run "main.py" to setup the config. Running the script again will cause the script to act like a bot which periodically checks the desired Subreddit.

2. Clone project and edit "main.py" to your liking. Removing the scheduler will cause the script to no longer act like a bot.
the
### Prerequisites

The requirements.txt file contains any Python dependencies. You can install them by running this command:

```
pip3 install -r requirements.txt
```

If you are attempting to run this on a Raspberry PI, be warned as there are many issues regarding the package Moviepy on ARM devices. I spent hours compiling and installing various packages to achieve any success with Moviepy.

## Built With

* [InstagramAPI](https://github.com/LevPasha/Instagram-API-python/)  - API to interface with Instagram
* [praw](https://praw.readthedocs.io/en/latest/) - Library to utilize Reddit API

## Contributing

Feel free to fork and make changes that will benefit the project!
