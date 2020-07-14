# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import os
from services.messenger import get_locale, get_timezone, get_main_menu
from fbmessenger import quick_replies


def test_webhook(client):
    """Test that the webhook URL is set correctly"""

    VERIFY_TOKEN = os.environ.get("FB_VERIFY_TOKEN", None)

    assert VERIFY_TOKEN is not None
    url = (
        "/webhook?hub.verify_token=" + VERIFY_TOKEN +
        "&hub.chalenge=CHALLENGE_ACCEPTED&hub.mode=subscribe&init_bot=true"
    )

    response = client.get(url)

    assert response.status_code == 202
    assert response.mimetype == "application/json"


def test_default_get_locale():
    """Test that we can extract the locale from user data"""
    assert get_locale() is "en"


def test_default_get_timezone():
    """Test that we can extract the timezone from user data"""
    assert get_timezone() is 0


def test_main_menu_OK():
    """Test that the main menu is well formatted"""
    main_menu = get_main_menu()

    assert isinstance(main_menu, quick_replies.QuickReplies)
    assert len(main_menu.quick_replies) < 11

    for qr in main_menu.quick_replies:
        assert isinstance(qr, quick_replies.QuickReply)
        assert len(qr.title) <= 20
        assert len(qr.payload) < 1000
