 # coding=utf-8
from __future__ import unicode_literals

import os
from time import sleep, time
import yaml, twitter

BRIEF_WAIT_SECS=2
LEEWAY_SECS=10

def main_loop(tweeter):
    while True:
        if the_line_lost_sync_again():
            downtime = time_operation(wait_for_it_to_come_back_up)
            if downtime > LEEWAY_SECS:
                tweeter.tweet(
                    passive_aggressive_message(downtime)
                )
        wait_briefly()

def the_line_lost_sync_again():
    hostname = "8.8.8.8"
    response = os.system("ping -c 1 " + hostname + ">/dev/null 2>&1")
    if response == 0: return False
    else: return True

def wait_for_it_to_come_back_up():
    while the_line_lost_sync_again():
        wait_briefly()

def time_operation(func):
    startTime = now()
    func()
    seconds_duration = now() - startTime
    return int(round(seconds_duration))

def wait_briefly():
    sleep(BRIEF_WAIT_SECS)

def now():
    return time()

def passive_aggressive_message(downtime):
    return "@plusnethelp Automated notification: My line just lost sync for " \
        + "%s seconds #embarrassing" % (downtime)

class Tweeter():
    def __init__(self, config_file):
        config = self.config_from_file(config_file)
        self.api = twitter.Api(consumer_key=config["consumer_key"],
                               consumer_secret=config["consumer_secret"],
                               access_token_key=config['access_token_key'],
                               access_token_secret=config['access_token_secret']
                               )
        self.api.VerifyCredentials()

    def config_from_file(self, config_file):
        with open(config_file) as f:
            return yaml.load(f)["twitter_config"]

    def tweet(self, tweet):
        self.api.PostUpdate('testing 123!!')
        

if __name__ == '__main__':
    tweeter = Tweeter("config.yaml")
    main_loop(tweeter)

