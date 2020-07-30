# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import os
import sys
import logging

from validators import url

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


GREETING = {
    "greeting": [
        {
            "locale": "default",
            "text": u'🙋🏽 Hi {{user_first_name}}! Click on the Get Started'
            ' button bellow to access Facebook DevC curated resources related'
            ' to Open Source 🔓.'
        },
        {
            "locale": "fr_FR",
            "text": u'🙋🏽 Salut {{user_first_name}}! Clique sur le bouton'
            ' Démarrer en dessous pour accéder à des resources collectées par'
            ' les DevC de Facebook relatives à l\'Open Source 🔓.'
        },
        {
            "locale": "hi_HI",
            "text": u'🙋🏽 नमस्ते {{user_first_name}}! ओपन सोर्स से संबंधित'
            ' फेसबुक देवसी क्यूरेट संसाधनों तक पहुंचने के लिए नीचे दिए गए'
            ' स्टार्ट बटन पर क्लिक करें 🔓।'
        }
    ]
}

PERSISTENT_MENU = {
    "persistent_menu": [
        {
            "locale": "default",
            "composer_input_disabled": False,
            "call_to_actions": [
                {
                    "type": "postback",
                    "title": "🏁 Start Over",
                    "payload": "START"
                },
                {
                    "type": "postback",
                    "title": "🗄️ Main Menu",
                    "payload": "MAIN_MENU"
                },
                {
                    "type": "postback",
                    "title": "🔓 FB Open Source",
                    "payload": "FB_OS"
                }
            ]
        },
        {
            "locale": "fr_FR",
            "composer_input_disabled": False,
            "call_to_actions": [
                {
                    "type": "postback",
                    "title": " 🏁 Redémarrer",
                    "payload": "START"
                },
                {
                    "type": "postback",
                    "title": "🗄️ Menu Principal",
                    "payload": "MAIN_MENU"
                },
                {
                    "type": "postback",
                    "title": "🔓 FB Open Source",
                    "payload": "FB_OS"
                }
            ]
        },
        {
            "locale": "hi_HI",
            "composer_input_disabled": False,
            "call_to_actions": [
                {
                    "type": "postback",
                    "title": "🏁 प्रारंभ करें",
                    "payload": "START"
                },
                {
                    "type": "postback",
                    "title": "🗄️ मुख्य मेनू",
                    "payload": "MAIN_MENU"
                },
                {
                    "type": "postback",
                    "title": "🔓 एफबी खुला स्रोत",
                    "payload": "FB_OS"
                }
            ]
        }
    ]
}


def get_white_listed_urls():
    """function to generate white listed url"""

    urls = []

    white_listed_urls = os.environ.get("WHITE_LISTED_URLS", None)
    if white_listed_urls:
        white_listed_urls = white_listed_urls.split(',')
        for u in white_listed_urls:
            if u.startswith('https://') and url(u):
                urls.append(u)

    app_url = os.environ.get('APP_URL', None)
    if app_url and app_url.startswith('https://') and url(app_url):
        urls.append(app_url)

    return urls


def init_profile(messenger):
    """Function to initialize chatbot profile"""

    white_listed_urls = get_white_listed_urls()
    res = messenger.add_whitelisted_domains(white_listed_urls)

    logger.debug('white_listed_urls: {}'.format(white_listed_urls))
    logger.debug('add_withelisted: {}'.format(res))

    res = messenger.set_messenger_profile(GREETING)
    logger.debug('GreetingText: {}'.format(GREETING))
    logger.debug('GreetingText: {}'.format(res))

    get_started = {
        "get_started": {
            "payload": "START"
        }
    }
    res = messenger.set_messenger_profile(get_started)
    logger.debug('GetStartedButton: {}'.format(get_started))
    logger.debug('GetStartedButton: {}'.format(res))

    res = messenger.set_messenger_profile(PERSISTENT_MENU)
    logger.debug('PersistentMenu: {}'.format(PERSISTENT_MENU))
    logger.debug('PersistentMenu: {}'.format(res))
