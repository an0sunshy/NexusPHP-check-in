#!/usr/bin/python3
import requests
import logging
import os
import hash_lookup
import time
import threading

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
USER_AGENT = '"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"'
HEADER = {'user-agent': USER_AGENT}
CONFIG_FILE = 'logins.conf'
WEEK_TO_SECOND = 60 * 60 * 24 * 7


class Website:
    def __init__(self, website, username, password):
        self.website = website
        self.username = username
        self.password = password


def load_config():
    config = []
    with open(CONFIG_FILE, 'r') as f:
        for line in f:
            login = line.strip().split(',')
            if len(login) != 3:
                continue
            config.append(Website(login[0], login[1], login[2]))
    return config if config else None


def get_image_string(h):
    return hash_lookup.lookup(h)


def login(website):
    # Query Imagehash
    logging.info('Logging %s...' % website.website)
    with requests.Session() as s:
        image_string = ""
        while len(image_string) != 6:
            r = s.get(website.website, headers=HEADER)
            if not r.ok:
                continue
            login_page = r.text
            h_start_index = login_page.find('imagehash=')
            image_hash = login_page[h_start_index + 10:h_start_index + 42]
            logging.info('Got ImageHash: %s' % image_hash)
            # Login
            image_string = get_image_string(image_hash)
            time.sleep(30)
        logging.info(
            'ImageHash %s decoded successfully -> %s' %
            (image_hash, image_string))
        payload = {
            'username': website.username,
            'password': website.password,
            'imagestring': image_string,
            'imagehash': image_hash}
        index_page = s.post(
            website.website +
            '/takelogin.php',
            headers=HEADER,
            data=payload)
        if index_page.ok:
            if '欢迎回来' in index_page.text or 'Welcome' in index_page.text or '歡迎回來' in index_page.text:
                logging.info('Logged In %s successfully!' % website.website)
        else:
            # time.sleep(60)
            logging.info('Retry in 60s')
            login(website)


if __name__ == '__main__':
    if not os.path.exists('dict'):
        logging.info(
            'No generated dictionaries found!\nGenerating dictionaries...')
        import gen_hash
        gen_hash.gen_hash()
        logging.info('Dictionaries Generated')
    if not os.path.exists(CONFIG_FILE):
        logging.fatal('No logins found!')
        exit(1)
    logins = load_config()
    if not logins:
        logging.fatal('No valid logins found!')
    for website in logins:
        login(website)
