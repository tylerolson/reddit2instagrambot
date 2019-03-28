import argparse
import logging
import schedule
import time
from reddit2instagram import reddit, instagram


def main(args):
    logger = logging.getLogger("main")

    handler = [h for h in logger.handlers if h.get_name() == "console_handler"][0]

    if args.verbose:
        handler.setLevel(handler.level - (args.verbose * 10))

    schedule.every().hour.do(downloadAndUpload)


def downloadAndUpload():
    reddit_conn = reddit.connect_reddit()
    found_subs = reddit.scrape_subreddit(reddit_conn, "RocketLeague")
    reddit.download_subs(found_subs)
    instagram.upload_subs(found_subs)


def process_args():
    parser = argparse.ArgumentParser(prog='reddit2instagram')
    parser.add_argument('-v', '--verbose', action='count',
                        help='Increase the verbosity level of the console')
    return parser.parse_args()


if __name__ == "__main__":
    args = process_args()
    main(args)

while True:
    schedule.run_pending()
    time.sleep(1)
