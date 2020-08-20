# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import os
import sys
import logging

from time import sleep
from flask import Blueprint, request, Response
from flask_babel import refresh, gettext as _

from fbmessenger import BaseMessenger, MessengerClient
from fbmessenger.templates import GenericTemplate
from fbmessenger.elements import Text, Button, Element
from fbmessenger import quick_replies
from fbmessenger.attachments import Image
from fbmessenger.sender_actions import SenderAction

from .profile import init_profile
from fbosbot import babel

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

DEFAULT_API_VERSION = "7.0"

bp = Blueprint("messenger", __name__)

# Let us set up a user as a global variable
# Default user values
user = {"first_name": _("Friend"), "locale": "en", "timezone": 0}

typing_on = SenderAction(sender_action="typing_on").to_dict()
typing_off = SenderAction(sender_action="typing_off").to_dict()
mark_seen = SenderAction(sender_action="mark_seen").to_dict()


@babel.localeselector
def get_locale():

    if "locale" in user:
        # ar_AR is not supported so we have to make an exception
        if user["locale"].startswith("ar_"):
            return "ar"

        return user["locale"]
    return "en"


@babel.timezoneselector
def get_timezone():
    if "timezone" in user:
        return user["timezone"]
    return 0


def init_user_preference(messenger):
    # Localise the bot for the current user
    list_of_globals = globals()
    list_of_globals["user"].update(messenger.get_user())
    logger.debug("Current USER: {}".format(user))

    get_locale()
    get_timezone()
    refresh()


def send_start_messages(messenger):
    """Function to launch at the start of restart of the chatbot"""

    txt = _(
        u"🙏🏼 Hi %(first_name)s, so you’ve decided to make your first steps in"
        " Open Source. That’s great.",
        **user
    )
    messenger.send({"text": txt}, "RESPONSE")
    messenger.send_action(typing_on)
    sleep(3)

    # A quick reply to the main menu
    qr1 = quick_replies.QuickReply(
        title=_("✔️ Yes"), payload="KNOW_OS_YES_FULL")
    qr2 = quick_replies.QuickReply(title=_("❌ Not yet"), payload="KNOW_OS_NO")
    qrs = quick_replies.QuickReplies(quick_replies=[qr1, qr2])
    text = {
        "text": _(
            u"So, tell me %(first_name)s do you know what Open Source"
            " is? 👇🏼", **user
        ),
        "quick_replies": qrs.to_dict(),
    }
    messenger.send(text, "RESPONSE")


def get_main_menu():
    """Function that returns the main menu of the chatbot"""
    open_source = quick_replies.QuickReply(
        title=_("Open Source 🔓"), payload="OPEN_SOURCE"
    )
    git = quick_replies.QuickReply(title=_("Git"), payload="GIT_0")
    github = quick_replies.QuickReply(title=_("GitHub"), payload="GITHUB_1")
    contr = quick_replies.QuickReply(title=_("Make a PR"), payload="CONTR_1")
    fb_os = quick_replies.QuickReply(
        title=_("FB Open Source"), payload="FB_OS")
    fork_me = quick_replies.QuickReply(
        title=_("Fork me on GitHub"), payload="FORK_ON_GITHUB"
    )

    return quick_replies.QuickReplies(
        quick_replies=[open_source, git, github, contr, fb_os, fork_me]
    )


def process_message(messenger, message):
    if "attachments" in message["message"]:
        if message["message"]["attachments"][0]["type"] == "location":
            logger.debug("Location received")
            attachments = message["message"]["attachments"]
            response = Text(
                text="{}: lat: {}, long: {}".format(
                    message["message"]["attachments"][0]["title"],
                    attachments[0]["payload"]["coordinates"]["lat"],
                    attachments[0]["payload"]["coordinates"]["long"],
                )
            )
            res = messenger.send(response.to_dict(), "RESPONSE")
            logger.debug("Response: {}".format(res))
            return True

    if (
        "quick_reply" in message["message"]
        and "payload" in message["message"]["quick_reply"]
    ):
        payload = message["message"]["quick_reply"]["payload"]
        process_postback(messenger, payload)
        return True

    text = None
    if "text" in message["message"]:
        msg = message["message"]["text"]
        if msg.lower() in ["help", "info"]:
            text = {
                "text": _(
                    u"Oh you need some help 🆘!"
                    " This is the main menu, select what you need below 👇🏼"
                ),
                "quick_replies": get_main_menu().to_dict(),
            }
        else:
            user["msg"] = msg
            text = {
                "text": _(
                    u"I didn't get you %(first_name)s"
                    "!\nYou said : %(msg)s\n"
                    "\nThis is the main menu, select what you need below 👇🏼",
                    **user
                ),
                "quick_replies": get_main_menu().to_dict(),
            }

    if not text:
        text = {
            "text": _(
                u"%(first_name)s\n"
                "This is the main menu, select what you need below 👇🏼"
            ),
            "quick_replies": get_main_menu().to_dict(),
        }

    messenger.send(text, "RESPONSE")
    return True


def process_postback(messenger, payload):
    """Function to process postbacks

    Args:
        messenger ([Messenger]): a Messenger Object
        payload ([Payload]): the payload sent by the user
    """
    init_user_preference(messenger)

    if "START" in payload:
        send_start_messages(messenger)
        return True

    if "MAIN_MENU" in payload:
        text = {
            "text": _(u"This is the main menu, select what you need below 👇🏼"),
            "quick_replies": get_main_menu().to_dict(),
        }
        messenger.send(text, "RESPONSE")
        return True

    if "OPEN_SOURCE" in payload:
        qr1 = quick_replies.QuickReply(
            title=_("✔️ Yes"), payload="KNOW_OS_YES_FULL")
        qr2 = quick_replies.QuickReply(
            title=_("❌ Not yet"), payload="KNOW_OS_NO")
        qrs = quick_replies.QuickReplies(quick_replies=[qr1, qr2])
        text = {
            "text": _(
                u"So, tell me %(first_name)s do you know what Open source"
                " is? 👇🏼", **user
            ),
            "quick_replies": qrs.to_dict(),
        }
        messenger.send(text, "RESPONSE")
        return True

    if payload.startswith("KNOW_OS_YES"):
        if "KNOW_OS_YES_FULL" in payload:
            messenger.send({"text": _(u"Amazing!")}, "RESPONSE")
            messenger.send_action(typing_on)
            sleep(3)

        qr1 = quick_replies.QuickReply(title=_("✔️ Yes"), payload="CVS_YES")
        qr2 = quick_replies.QuickReply(title=_("❌ Not yet"), payload="CVS_NO")
        qrs = quick_replies.QuickReplies(quick_replies=[qr1, qr2])
        text = {
            "text": _(
                u"An important component in Open Source contribution is"
                " version control tools. Are you familiar with the concept of"
                " version control? 👇🏼"
            ),
            "quick_replies": qrs.to_dict(),
        }
        messenger.send(text, "RESPONSE")
        return True

    if "KNOW_OS_NO" in payload:
        text = _(
            u"According to the dictionary, Open-source 🔓 software, denotes"
            " software for which the original source code is made freely 🆓"
            " available and may be redistributed and modified"
            " according to the requirement of the user 👨‍💻."
        )
        messenger.send({"text": text}, "RESPONSE")
        messenger.send_action(typing_on)
        sleep(3)

        qr = quick_replies.QuickReply(
            title=_("👉🏽 Next"), payload="KNOW_OS_YES")
        qrs = quick_replies.QuickReplies(quick_replies=[qr])
        text = {
            "text": _(
                u'👩🏽‍🏫 You know ...\n✔️ Wordpress,\n✔️ Notepad++,\n✔️ Ubuntu\n'
                'and thousands of common software started out as Open-source'
                ' software? 👇🏼'
            ),
            "quick_replies": qrs.to_dict(),
        }
        messenger.send(text, "RESPONSE")
        return True

    if "CVS_NO" in payload:
        text = {
            "text": _(
                u"😎 Worry not!\n\n"
                "Version control allows you to manage changes to files over"
                " time ⏱️ so that you can recall specific versions later."
            )
        }
        messenger.send(text, "RESPONSE")
        messenger.send_action(typing_on)
        sleep(3)
        text = {
            "text": _(
                u"You can use version control to version code, binary files,"
                " and digital assets 🗄️."
            )
        }
        messenger.send(text, "RESPONSE")
        messenger.send_action(typing_on)
        sleep(3)
        text = {
            "text": _(
                u"This includes version control software, version control"
                " systems, or version control tools 🧰."
            )
        }
        messenger.send(text, "RESPONSE")
        messenger.send_action(typing_on)
        sleep(3)
        text = {
            "text": _(
                u"Version control is a component of software configuration"
                " management 🖥️."
            )
        }
        messenger.send(text, "RESPONSE")
        messenger.send_action(typing_on)
        sleep(3)
        qr = quick_replies.QuickReply(title=_("👉🏽 Next"), payload="CVS_YES")
        qrs = quick_replies.QuickReplies(quick_replies=[qr])
        text = {
            "text": _(
                u"😎 Now that you understand what Version control is,"
                " let's explore another important topic."
            ),
            "quick_replies": qrs.to_dict(),
        }
        messenger.send(text, "RESPONSE")
        return True

    if "CVS_YES" in payload:
        qr1 = quick_replies.QuickReply(
            title=_("What is Git❔"), payload="GIT_1")
        qr2 = quick_replies.QuickReply(
            title=_("What is GitHub❔"), payload="GITHUB_1")
        qrs = quick_replies.QuickReplies(quick_replies=[qr1, qr2])
        text = {
            "text": _(u"What do you want to start with⁉️ 👇🏼"),
            "quick_replies": qrs.to_dict(),
        }
        messenger.send(text, "RESPONSE")
        return True

    if "GITHUB_1" in payload:
        qr = quick_replies.QuickReply(title=_("👉🏽 Next"), payload="GITHUB_2")
        qrs = quick_replies.QuickReplies(quick_replies=[qr])
        text = {
            "text": _(
                u"GitHub is a code hosting platform for version control and"
                " collaboration. It lets you and others work together on"
                " projects from anywhere."
            ),
            "quick_replies": qrs.to_dict(),
        }
        messenger.send(text, "RESPONSE")
        return True

    if "GITHUB_2" in payload:
        btn1 = Button(
            button_type="web_url",
            title=_("Official Website"),
            url="https://github.com"
        )
        btn2 = Button(
            button_type="web_url",
            title=_("GitHub Tutorial"),
            url="https://guides.github.com/activities/hello-world/",
        )
        btn3 = Button(
            button_type="postback",
            title=_("👩‍💻 Make a PR"),
            payload="CONTR_1"
        )
        app_url = os.environ.get("APP_URL", "localhost")
        elems = Element(
            title=_(u"Discover GitHub"),
            image_url=app_url + "/static/img/github.jpg",
            subtitle=_(
                u"Discover GitHub official website, or follow a beginner"
                " tutorial",
            ),
            # Messenger only accepts 3 buttons, hard choice to make!
            buttons=[btn1, btn2, btn3],
        )
        res = GenericTemplate(elements=[elems])
        logger.debug(res.to_dict())
        messenger.send(res.to_dict(), "RESPONSE")
        return True

    if payload.startswith("GIT_"):
        if "GIT_1" in payload:
            messenger.send({"text": _("Good question 👌🏽")}, "RESPONSE")
            messenger.send_action(typing_on)
            sleep(3)

            text = _(
                u"Git is a type of version control system (VCS) that makes"
                " it easier to track changes to files. "
            )
            messenger.send({"text": text}, "RESPONSE")
            messenger.send_action(typing_on)
            sleep(3)

            text = _(
                u"For example, when you edit a file, Git can help you"
                " determine exactly what changed, who changed it, and why."
            )
            messenger.send({"text": text}, "RESPONSE")
            messenger.send_action(typing_on)
            sleep(3)

            qr1 = quick_replies.QuickReply(
                title=_("👶🏽 Install Git"), payload="INSTALL_GIT"
            )
            qr2 = quick_replies.QuickReply(
                title=_("🤓 I've Git Installed"), payload="CONF_GIT"
            )
            qrs = quick_replies.QuickReplies(quick_replies=[qr1, qr2])
            text = {
                "text": _(u"Want to learn more about Git?"),
                "quick_replies": qrs.to_dict(),
            }
            messenger.send(text, "RESPONSE")
            return True

    ###################################
    # FIRST TIME CONTRIBUTION SECTION #
    ###################################
    # Guiding users to this first time contribution
    if payload.startswith("CONTR_"):

        if "CONTR_1" in payload:
            messenger.send({"text": _("Good decision 👌🏽")}, "RESPONSE")
            messenger.send_action(typing_on)
            sleep(3)

            text = _(
                u"We are going to split the process into 5 steps: \n"
                "🛵 Fork, Clone, Update, Push and Merge. "
            )
            messenger.send({"text": text}, "RESPONSE")
            messenger.send_action(typing_on)
            sleep(3)

            qr = quick_replies.QuickReply(
                title=_("🥢 1. Fork"), payload="CONTR_2")
            qrs = quick_replies.QuickReplies(quick_replies=[qr])
            text = {
                "text": _(u"Ready for the first step?!"),
                "quick_replies": qrs.to_dict(),
            }
            messenger.send(text, "RESPONSE")
            return True

        # Fork Step
        if "CONTR_2" in payload:
            messenger.send({"text": _("Awesome 👌🏽")}, "RESPONSE")
            messenger.send_action(typing_on)
            sleep(3)

            text = _(
                u"Open this link in a new window: \n"
                "https://github.com/fbdevelopercircles/open-source-edu-bot"
            )
            messenger.send({"text": text}, "RESPONSE")
            messenger.send_action(typing_on)
            sleep(3)
            text = _(
                u"Now, click `Fork` on the top right corner of your screen"
            )
            messenger.send({"text": text}, "RESPONSE")
            image = Image(
                url="https://docs.github.com/assets/images/help/repository/"
                "fork_button.jpg"
            )
            messenger.send(image.to_dict(), "RESPONSE")
            messenger.send_action(typing_on)
            text = _(
                u"A copy of the original project will be created in your"
                " account."
            )
            messenger.send({"text": text}, "RESPONSE")
            messenger.send_action(typing_on)
            sleep(3)
            qr = quick_replies.QuickReply(
                title=_("🚃 2. Clone"), payload="CONTR_3_1")
            qrs = quick_replies.QuickReplies(quick_replies=[qr])
            text = {
                "text": _(u"Ready for the next step?!"),
                "quick_replies": qrs.to_dict(),
            }
            messenger.send(text, "RESPONSE")
            return True

        # Clone Step
        if "CONTR_3_1" in payload:
            messenger.send({"text": _("Great 👌🏽")}, "RESPONSE")
            messenger.send_action(typing_on)
            sleep(3)

            text = _(
                u"Right now, you have a fork of the `open-source-edu-bot`"
                " repository, but you don't have the files in that repository"
                " on your computer."
            )
            messenger.send({"text": text}, "RESPONSE")
            messenger.send_action(typing_on)
            sleep(3)
            text = _(
                u"Let's create a clone of your fork locally on your computer."
                "\nOn GitHub, in your newly forked project, Click on `Code`"
                " above the list of files"
            )
            messenger.send({"text": text}, "RESPONSE")
            image = Image(
                url="https://docs.github.com/assets/images/help/repository/"
                "code-button.png"
            )
            messenger.send(image.to_dict(), "RESPONSE")

            qr = quick_replies.QuickReply(
                title=_("👉🏽 Next"), payload="CONTR_3_2")
            qrs = quick_replies.QuickReplies(quick_replies=[qr])
            text = {
                "text": _(u"When you feel Ready🔥, hit Next to continue."),
                "quick_replies": qrs.to_dict(),
            }
            messenger.send(text, "RESPONSE")
            return True
        if "CONTR_3_2" in payload:
            text = _(
                u'To clone the repository using HTTPS, under'
                ' "Clone with HTTPS", click copy icon.\n'
                'To clone the repository using an SSH key click "Use SSH", '
                'then click on copy icon.'
            )
            messenger.send({"text": text}, "RESPONSE")
            image = Image(
                url="https://docs.github.com/assets/"
                "images/help/repository/https-url-clone.png"
            )
            messenger.send(image.to_dict(), "RESPONSE")
            messenger.send_action(typing_on)
            sleep(3)
            text = _(
                u"Now open a terminal, change the current working directory"
                " to the location where you want the cloned directory."
            )
            messenger.send({"text": text}, "RESPONSE")
            messenger.send_action(typing_on)
            sleep(3)
            text = _(
                u"Type `git clone`, and then paste the URL you copied "
                "earlier.\nPress Enter. Your local clone will be created."
            )
            messenger.send({"text": text}, "RESPONSE")
            messenger.send_action(typing_on)
            qr = quick_replies.QuickReply(
                title=_("🥯 3. Update"), payload="CONTR_4")
            qrs = quick_replies.QuickReplies(quick_replies=[qr])
            text = {
                "text": _(
                    u"Now, you have a local copy of the project, Let's update"
                    " it!"
                ),
                "quick_replies": qrs.to_dict(),
            }
            messenger.send(text, "RESPONSE")
            return True

        # Update Step
        if "CONTR_4" in payload:
            messenger.send({"text": _("Amazing 👌🏽")}, "RESPONSE")
            messenger.send_action(typing_on)
            sleep(3)

            text = _(
                u"Open the project using your favorite IDE, and look for"
                " `contributors.yaml` file"
            )
            messenger.send({"text": text}, "RESPONSE")
            messenger.send_action(typing_on)
            sleep(3)
            text = _(
                u"This Yaml file contains list of project contributors,"
                " just like you."
            )
            messenger.send({"text": text}, "RESPONSE")
            messenger.send_action(typing_on)
            image = Image(
                url="https://media.giphy.com/media/UsBYak2l75W5VheVPF/"
                "giphy.gif"
            )
            messenger.send(image.to_dict(), "RESPONSE")
            text = _(
                u"Following the same scheme, add your name, country and github"
                " username to the list."
            )
            messenger.send({"text": text}, "RESPONSE")
            messenger.send_action(typing_on)
            sleep(3)
            qr = quick_replies.QuickReply(
                title=_("🚲 4. Push"), payload="CONTR_5")
            qrs = quick_replies.QuickReplies(quick_replies=[qr])
            text = {
                "text": _(u"Ready to commit & Push your changes?!"),
                "quick_replies": qrs.to_dict(),
            }
            messenger.send(text, "RESPONSE")
            return True

        # Push Step
        if "CONTR_5" in payload:
            messenger.send({"text": _("Way to go 👌🏽")}, "RESPONSE")
            messenger.send_action(typing_on)
            sleep(3)
            text = _(
                u"Open your Terminal.\nChange the current working directory"
                " to your local repository."
                "\nStage the file by commiting it to your"
                " local repository using: `git add .`"
            )
            messenger.send({"text": text}, "RESPONSE")
            messenger.send_action(typing_on)
            sleep(3)
            text = _(
                u'Commit the file that you\'ve staged in your local'
                ' repository:\n'
                '`git commit -m "Add YOUR_NAME to contributors list"`\n'
                "Make sure to add your name :D"
            )
            messenger.send({"text": text}, "RESPONSE")
            messenger.send_action(typing_on)
            sleep(3)
            text = _(
                u"Finally, Push the changes in your local repository to "
                " GitHub: `git push origin master`"
            )
            messenger.send({"text": text}, "RESPONSE")
            messenger.send_action(typing_on)
            sleep(3)
            qr = quick_replies.QuickReply(
                title=_("🔐 5. Merge"), payload="CONTR_6")
            qrs = quick_replies.QuickReplies(quick_replies=[qr])
            text = {
                "text": _(u"Ready to make your first PR?!"),
                "quick_replies": qrs.to_dict(),
            }
            messenger.send(text, "RESPONSE")
            return True

        # Merge Step
        if "CONTR_6" in payload:
            messenger.send({"text": _("Proud of you 👌🏽")}, "RESPONSE")
            messenger.send_action(typing_on)
            sleep(3)
            text = _(
                u"Now go back to the original repo:"
                " https://github.com/fbdevelopercircles/open-source-edu-bot \n"
                "Above the list of files, click `Pull request`."
            )
            messenger.send({"text": text}, "RESPONSE")
            primg = Image(
                url="https://docs.github.com/assets/images/help/"
                "pull_requests/pull-request-start-review-button.png"
            )
            messenger.send(primg.to_dict(), "RESPONSE")
            messenger.send_action(typing_on)
            sleep(3)
            text = _(
                u'Make sure that "base branch" & "head fork" drop-down menus'
                ' both are pointing to `master`.'
            )
            messenger.send({"text": text}, "RESPONSE")
            messenger.send_action(typing_on)
            sleep(3)
            prdesc = Image(
                url="https://docs.github.com/assets/images/help/"
                "pull_requests/pullrequest-description.png"
            )
            messenger.send(prdesc.to_dict(), "RESPONSE")
            text = _(
                u"Type a title and description for your pull request."
                " Then click `Create Pull Request`."
            )
            messenger.send({"text": text}, "RESPONSE")
            messenger.send_action(typing_on)
            qr = quick_replies.QuickReply(title=_("✅ Done"), payload="CONTR_7")
            qrs = quick_replies.QuickReplies(quick_replies=[qr])
            text = {
                "text": _(u"Have you created your first PR?"),
                "quick_replies": qrs.to_dict(),
            }
            messenger.send(text, "RESPONSE")
            return True

        # Merge Step
        if "CONTR_7" in payload:
            messenger.send(
                {
                    "text": _("🙌🎉 Bravo %(first_name)s 🙌🎉", **user)
                },
                "RESPONSE"
            )
            messenger.send_action(typing_on)
            sleep(3)
            response = Image(
                url="https://media.giphy.com/media/MOWPkhRAUbR7i/giphy.gif"
            )
            messenger.send(response.to_dict(), "RESPONSE")
            messenger.send(
                {
                    "text": _(
                        "Now the team will review your PR and merge it ASAP :D"
                    )
                },
                "RESPONSE",
            )
            messenger.send_action(typing_on)
            sleep(3)
            text = {
                "text": _(
                    u"Given below are other interesting stuff"
                    " that we can explore together:"
                ),
                "quick_replies": get_main_menu().to_dict(),
            }
            messenger.send(text, "RESPONSE")
            return True

    if payload.startswith("GIT_"):
        if "GIT_1" in payload:
            messenger.send({"text": _("Good question 👌🏽")}, "RESPONSE")
            messenger.send_action(typing_on)
            sleep(3)

        text = _(
            u"Git is a type of version control system (VCS) that makes it"
            " easier to track changes to files. "
        )
        messenger.send({"text": text}, "RESPONSE")
        messenger.send_action(typing_on)
        sleep(3)

        text = _(
            u"For example, when you edit a file, Git can help you determine"
            " exactly what changed, who changed it, and why."
        )
        messenger.send({"text": text}, "RESPONSE")
        messenger.send_action(typing_on)
        sleep(3)

        qr1 = quick_replies.QuickReply(
            title=_("👶🏽 Install Git"), payload="INSTALL_GIT")
        qr2 = quick_replies.QuickReply(
            title=_("🤓 I've Git Installed"), payload="CONF_GIT"
        )
        qrs = quick_replies.QuickReplies(quick_replies=[qr1, qr2])
        text = {
            "text": _(u"Want to learn more about Git?"),
            "quick_replies": qrs.to_dict(),
        }
        messenger.send(text, "RESPONSE")
        return True

    if "INSTALL_GIT" in payload:

        text = _(u"Time to get Git installed in your machine ⭕!")
        messenger.send({"text": text}, "RESPONSE")
        messenger.send_action(typing_on)
        sleep(3)
        btn = Button(
            button_type="web_url",
            title=_("Download Git"),
            url="https://git-scm.com/downloads",
        )
        elems = Element(
            title=_(u"Head over here, and download Git"
                    " Client based on your OS."),
            buttons=[btn],
        )
        res = GenericTemplate(elements=[elems])
        logger.debug(res.to_dict())
        messenger.send(res.to_dict(), "RESPONSE")
        messenger.send_action(typing_on)
        sleep(3)
        qr2 = quick_replies.QuickReply(
            title=_("Configure Git ⚒️"), payload="CONF_GIT")
        qrs = quick_replies.QuickReplies(quick_replies=[qr2])
        text = {
            "text": _(u"🧑‍🚀 Once done, let's configure Git"),
            "quick_replies": qrs.to_dict(),
        }
        messenger.send(text, "RESPONSE")
        return True

    if "CONF_GIT" in payload:

        text = _(u"Great Progress so far 👨🏽‍🎓!")
        messenger.send({"text": text}, "RESPONSE")
        messenger.send_action(typing_on)
        sleep(2)
        text = _(
            u"Now let's configure your Git username and email using the"
            " following commands"
        )
        messenger.send({"text": text}, "RESPONSE")
        messenger.send_action(typing_on)
        sleep(2)
        text = _(u'`$ git config --global user.name "Steve Josh"`')
        messenger.send({"text": text}, "RESPONSE")
        messenger.send_action(typing_on)
        sleep(2)
        text = _(u'`$ git config --global user.email "josh@example.com"`')
        messenger.send({"text": text}, "RESPONSE")
        messenger.send_action(typing_on)
        sleep(2)
        text = _(
            u"Don't forget to replace Steve's  name and email with your own."
        )
        messenger.send({"text": text}, "RESPONSE")
        messenger.send_action(typing_on)
        sleep(2)
        text = _(
            u"These details will be associated with any commits that you"
            " create"
        )
        messenger.send({"text": text}, "RESPONSE")
        messenger.send_action(typing_on)
        sleep(2)
        qr = quick_replies.QuickReply(title=_("GitHub"), payload="GITHUB_1")
        qrs = quick_replies.QuickReplies(quick_replies=[qr])
        text = {
            "text": _(u"Now let's check, what is Github?👇🏼"),
            "quick_replies": qrs.to_dict(),
        }
        messenger.send(text, "RESPONSE")
        return True

    if "FB_OS" in payload:
        text = _(u"Facebook 🧡 Open Source!")
        messenger.send({"text": text}, "RESPONSE")
        sleep(3)

        text = _(
            u"Facebook manages many Open Source projects in the following"
            " areas:\n"
            "✔️ Android\n"
            "✔️ Artificial Intelligence\n"
            "✔️ Data Infrastructure\n"
            "✔️ Developer Operations\n"
            "✔️ Development Tools\n"
            "✔️ Frontend\n"
            "✔️ iOS\n"
            "✔️ Languages\n"
            "✔️ Linux\n"
            "✔️ Security\n"
            "✔️ Virtual Reality\n"
            "..."
        )
        messenger.send({"text": text}, "RESPONSE")
        sleep(3)

        btn = Button(
            button_type="web_url",
            title=_("Explore them"),
            url="https://opensource.facebook.com/projects",
        )
        elems = Element(
            title=_(u"Explore Facebook Open Source projects"), buttons=[btn]
        )
        res = GenericTemplate(elements=[elems])
        logger.debug(res.to_dict())
        messenger.send(res.to_dict(), "RESPONSE")

        return True

    if "FORK_ON_GITHUB" in payload:
        text = _(
            u"🤓 You know what? This chatbot code is Open Source 🔓, it's"
            " developed by Facebook Developers Circles members around the"
            " world."
        )
        messenger.send({"text": text}, "RESPONSE")
        sleep(5)

        text = _(
            u"%(first_name)s we welcome contributors, or simply feel free to"
            " fork the code on GitHub, and create your own chatbot.",
            **user
        )
        messenger.send({"text": text}, "RESPONSE")
        sleep(5)

        btn1 = Button(
            button_type="web_url",
            title=_("The Source Code"),
            url="https://github.com/fbdevelopercircles/open-source-edu-bot",
        )
        btn2 = Button(
            button_type="web_url",
            title=_("Join a circle"),
            url="https://developers.facebook.com/developercircles",
        )
        btn3 = Button(
            button_type="postback",
            title=_("🚶🏽‍♀️ Main Menu 🗄️"),
            payload="MAIN_MENU"
        )
        elems = Element(title=_(u"Select an option 👇🏼"),
                        buttons=[btn1, btn2, btn3])
        res = GenericTemplate(elements=[elems])
        logger.debug(res.to_dict())
        messenger.send(res.to_dict(), "RESPONSE")

        return True

    # the default action
    qr = quick_replies.QuickReply(
        title=_("🚶🏽‍♀️ Main Menu 🗄️"), payload="MAIN_MENU")
    qrs = quick_replies.QuickReplies(quick_replies=[qr])
    text = {"text": _(u"Coming soon!"), "quick_replies": qrs.to_dict()}
    messenger.send(text, "RESPONSE")
    return False


class Messenger(BaseMessenger):
    def __init__(self, page_access_token, app_secret=None, **kwargs):
        self.page_access_token = page_access_token
        self.app_secret = app_secret
        self.client = MessengerClient(
            self.page_access_token,
            app_secret=self.app_secret,
            api_version=kwargs.get("api_version", DEFAULT_API_VERSION),
        )
        # super(Messenger, self).__init__(self.page_access_token)

    def message(self, message):
        process_message(self, message)

    def delivery(self, message):
        pass

    def read(self, message):
        pass

    def account_linking(self, message):
        pass

    def postback(self, message):
        payload = message["postback"]["payload"]
        process_postback(self, payload)

    def optin(self, message):
        pass

    def init_bot(self):
        init_profile(self)


messenger = Messenger(
    os.environ.get("FB_PAGE_TOKEN"),
    api_version=DEFAULT_API_VERSION
)


@bp.route("/webhook", methods=["GET", "POST"])
def webhook():

    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        init_bot = request.args.get("init_bot", False)

        # Checks if a token and mode is in the query string of the request
        if mode and token:
            if (
                mode == 'subscribe' and
                token == os.environ.get('FB_VERIFY_TOKEN')
            ):
                logger.debug("CHALLENGE_ACCEPTED")

                if init_bot:
                    logger.debug('BOT INITIALISATION')
                    messenger.init_bot()

                return Response(
                    challenge,
                    status=202,
                    mimetype="application/json"
                )
            return challenge
        raise ValueError("FB_VERIFY_TOKEN does not match.")
    elif request.method == "POST":
        message = request.get_json(force=True)
        logger.debug("Message : {}".format(message))
        messenger.handle(message)
    return ""
