# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from services import profile


def test_get_white_listed_urls():
    """Test the generation of white listed url"""
    white_listed_urls = profile.get_white_listed_urls()

    assert isinstance(white_listed_urls, list)
