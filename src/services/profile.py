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
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


GREETING = {
    "greeting": [
        {
            "locale": "default",
            "text": u"🙋🏽 Hi {{user_first_name}}! Click on the Get Started"
            " button below to access Facebook DevC curated resources related"
            " to Open Source 🔓."
        },
        {
            "locale": "fr_FR",
            "text": u"🙋🏽 Salut {{user_first_name}}! Clique sur le bouton"
            " Démarrer en dessous pour accéder à des resources collectées par"
            " les DevC de Facebook relatives à l\"Open Source 🔓."
        },
        {
            "locale": "hi_IN",
            "text": u"🙋🏽 नमस्ते {{user_first_name}}! ओपन सोर्स से संबंधित"
            " फेसबुक देवसी क्यूरेट संसाधनों तक पहुंचने के लिए नीचे दिए गए"
            " स्टार्ट बटन पर क्लिक करें 🔓।"
        },
        {
            "locale": "si_LK",
            "text": u"🙋🏽 ආයුබෝවන් {{user_first_name}}! විවෘත මූලාශ්‍ර 🔓 වලට"
            " අදාල Facebook DevC වලින් ලබාදෙන සම්පත් වලට ප්‍රවේශ වෙන්න,"
            " Get Started බටන් එක ක්ලික් කරන්න."
        },
        {
            "locale": "rw_RW",
            "text": u"🙋🏽 Muraho {{user_first_name}}! Kanda hepho kuri Buto "
            "yo gutangira kugirango ugere ku bikoresho byegeranyijwe na "
            "Facebook DevC bijyanye na Open Source 🔓."
        },
        {
            "locale": "ar_AR",
            "text": u" 🙋🏽 "
            u" أهلا "
            u" {{user_first_name}}! "
            u" انقر فوق زر البدء أدناه "
            " للوصول إلى الموارد المنسقة من دوائر مطوري فيسبوك "
            " والمتعلقة بالمصادر المفتوحة "
            " .🔓 "
        },
        {
            "locale": "gu_IN",
            "text": u"🙋🏽 નમસ્તે {{user_first_name}}! ઓપન સોર્સ થી સંબંધિત "
            "ફેસબુક ડેવલપર સર્કલ્સ ક્યુરેટેડ સ્ત્રોતોને લગતા વપરાશ માટે "
            "નીચે પ્રારંભ કરો બટન પર ક્લિક કરો 🔓."
        },
        {
            "locale": "es_LA",
            "text": u"🙋🏽 ¡Hola {{user_first_name}}! Haz click en el botón de"
            " Empezar abajo para acceder a los recursos seleccionados de"
            " Facebook DevC relacionados con el Open Source 🔓."
        },
        {
            "locale": "ru_RU",
            "text": u"🙋🏽 Здравствуйте {{user_first_name}}! Нажмите Начать,"
            " кнопку ниже, чтобы получить доступ к ресурсам"
            " DevC Facebook, связанным с миром Open Source 🔓."
        },
        {
        "locale": "ta_IN",
            "text": u"🙋🏽 வணக்கம் {{user_first_name}}!திறந்த பேஸ்புக் வளங்கள், "
            "தொடர்பாக பேஸ்புக் டெவலப்பர் ,சமூகம் உருவாக்கிய வளங்களை அணுக"
            "கீழே உள்ள தொடங்கு பட்டனை கிளிக் செய்யவும் 🔓."
            
        
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
            "locale": "hi_IN",
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
                    "title": "🔓 एफबी ओपन सोर्स",
                    "payload": "FB_OS"
                }
            ]
        },
        {
            "locale": "si_LK",
            "composer_input_disabled": False,
            "call_to_actions": [
                {
                    "type": "postback",
                    "title": "🏁 ආයෙ මුල ඉඳන් පටං ගන්න",
                    "payload": "START"
                },
                {
                    "type": "postback",
                    "title": "🗄️ ප්‍රධාන මෙනුව",
                    "payload": "MAIN_MENU"
                },
                {
                    "type": "postback",
                    "title": "🔓 FB විවෘත මූලාශ්‍ර",
                    "payload": "FB_OS"
                }
            ]
        },
        {
            "locale": "rw_RW",
            "composer_input_disabled": False,
            "call_to_actions": [
                {
                    "type": "postback",
                    "title": "🏁 Tangira hejuru",
                    "payload": "START"
                },
                {
                    "type": "postback",
                    "title": "🗄️ Ibikubiyemo",
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
            "locale": "ar_AR",
            "composer_input_disabled": False,
            "call_to_actions": [
                {
                    "type": "postback",
                    "title": "🏁 ابدأ من جديد ",
                    "payload": "START"
                },
                {
                    "type": "postback",
                    "title": "🗄️ القائمة الرئيسية ",
                    "payload": "MAIN_MENU"
                },
                {
                    "type": "postback",
                    "title": "🔓 فيسبوك مفتوح المصدر ",
                    "payload": "FB_OS"
                }
            ]
        },
        {
            "locale": "gu_IN",
            "composer_input_disabled": False,
            "call_to_actions": [
                {
                    "type": "postback",
                    "title": "🏁 પ્રારંભ કરો",
                    "payload": "START"
                },
                {
                    "type": "postback",
                    "title": "🗄️ મુખ્ય મેનુ",
                    "payload": "MAIN_MENU"
                },
                {
                    "type": "postback",
                    "title": "🔓 એફબી ઓપન સોર્સ",
                    "payload": "FB_OS"
                }
            ]
        },
        {
            "locale": "es_LA",
            "composer_input_disabled": False,
            "call_to_actions": [
                {
                    "type": "postback",
                    "title": " 🏁 Empezar",
                    "payload": "START"
                },
                {
                    "type": "postback",
                    "title": "🗄️ Menú Principal",
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
            "locale": "ru_RU",
            "composer_input_disabled": False,
            "call_to_actions": [
                {
                    "type": "postback",
                    "title": "🏁 Начать",
                    "payload": "START"
                },
                {
                    "type": "postback",
                    "title": "🗄️ Главное меню",
                    "payload": "MAIN_MENU"
                },
                {
                    "type": "postback",
                    "title": "🔓 FB Open Source",
                    "payload": "FB_OS"
                },
                {
            "locale": "ta-IN",
            "composer_input_disabled": False,
            "call_to_actions": [
                {
                    "type": "postback",
                    "title": "🏁 மீண்டும் தொடங்குங்கள்",
                    "payload": "START"
                },
                {
                    "type": "postback",
                    "title": "🗄️ மெய்ன் மெனு",
                    "payload": "MAIN_MENU"
                },
                {
                    "type": "postback",
                    "title": "🔓 திறந்த மூல பேஸ்புக் வளங்கள்",
                    "payload": "FB_OS"
                }
            ]
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
        white_listed_urls = white_listed_urls.split(",")
        for u in white_listed_urls:
            if u.startswith("https://") and url(u):
                urls.append(u)

    app_url = os.environ.get("APP_URL", None)
    if app_url and app_url.startswith("https://") and url(app_url):
        urls.append(app_url)

    return urls


def init_profile(messenger):
    """Function to initialize chatbot profile"""

    white_listed_urls = get_white_listed_urls()
    res = messenger.add_whitelisted_domains(white_listed_urls)

    logger.debug("white_listed_urls: {}".format(white_listed_urls))
    logger.debug("add_withelisted: {}".format(res))

    res = messenger.set_messenger_profile(GREETING)
    logger.debug("GreetingText: {}".format(GREETING))
    logger.debug("GreetingText: {}".format(res))

    get_started = {
        "get_started": {
            "payload": "START"
        }
    }
    res = messenger.set_messenger_profile(get_started)
    logger.debug("GetStartedButton: {}".format(get_started))
    logger.debug("GetStartedButton: {}".format(res))

    res = messenger.set_messenger_profile(PERSISTENT_MENU)
    logger.debug("PersistentMenu: {}".format(PERSISTENT_MENU))
    logger.debug("PersistentMenu: {}".format(res))
