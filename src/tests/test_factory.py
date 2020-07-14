# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from fbosbot import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing
