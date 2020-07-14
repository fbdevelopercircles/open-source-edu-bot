# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from setuptools import find_packages, setup

setup(
    name='fbosbot',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "Flask>=1.1.2,<1.2.0",
        "fbmessenger>=6.0.0,<6.1",
        "six>=1.15.0,<1.16",
        "validators>=0.15.0,<0.16",
        "Flask-Babel>=1.0.0,<1.1.0"
    ],
)
