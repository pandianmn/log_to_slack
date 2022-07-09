# -*- coding: utf-8 -*-
import os

from setuptools import setup

VERSION = "1.8.1"


def readme(*paths):
    with open(os.path.join(*paths), "r") as f:
        return f.read()


def requirements(*paths):
    with open(os.path.join(*paths), "r") as f:
        return list(line.strip() for line in f.readlines() if line.strip() != "")


setup(
    name="log_to_slack",
    packages=["log_to_slack"],
    version=VERSION,
    description="Posts log events to Slack via API",
    long_description=readme("README.rst"),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Communications :: Chat",
        "Topic :: Office/Business :: Groupware",
    ],
    url="https://github.com/pandianmn/log_to_slack",
    download_url="https://github.com/pandianmn/log_to_slack/archive/{v}.tar.gz".format(
        v=VERSION
    ),
    author="Pandian Muninathan",
    author_email="pandian.m@hotmail.com",
    keywords=["slack", "logging"],
    install_requires=requirements("requirements.txt"),
    include_package_data=True,
    zip_safe=False,
)
