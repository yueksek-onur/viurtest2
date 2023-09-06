#!/usr/bin/python
#
#                 iii
#                iii
#               iii
#
#           vvv iii uu      uu rrrrrrrr
#          vvvv iii uu      uu rr     rr
#   v     vvvv  iii uu      uu rr     rr
#  vvv   vvvv   iii uu      uu rr rrrrr
# vvvvv vvvv    iii uu      uu rr rrr
#  vvvvvvvv     iii uu      uu rr  rrr
#   vvvvvv      iii  uu    uu  rr   rrr
#    vvvv       iii   uuuuuu   rr    rrr
#
#   I N F O R M A T I O N    S Y S T E M
# ------------------------------------------------------------------------------
#
# Project:      viurtest2
# Initiated:    2023-09-01 06:00:44
# Copyright:    onur @ Mausbrand Informationssysteme GmbH
# Author:       onur
#
# ------------------------------------------------------------------------------

import os, logging
from viur import core
from viur.core import current,conf, email, securityheaders
from viur.core.modules.file import thumbnailer

# ------------------------------------------------------------------------------
# General configuration
#

conf["viur.validApplicationIDs"] = ["viurtest2"]

# ------------------------------------------------------------------------------
# Debugging & Performance
#

# conf["viur.disableCache"] = True
# conf["viur.debug.traceQueries"] = True
# conf["viur.debug.traceExternalCallRouting"] = True
# conf["viur.debug.traceExceptions"] = True

# VIUR<3.4 compatibility feature disabling
# conf["viur.compatibility"].remove("json.bone.structure.keytuples")  # render new dict-style bone-structure
# conf["viur.compatibility"].remove("json.bone.structure.camelcasenames")  # render new keys in bone structure only

# ------------------------------------------------------------------------------
# File module
#

# By default, file download URLs do not expire.
# Comment this in if you store sensitive files that should not be public.
# from datetime import timedelta
# conf["viur.render.html.downloadUrlExpiration"] = timedelta(hours=1)
# conf["viur.render.json.downloadUrlExpiration"] = timedelta(hours=1)

conf["viur.file.derivers"] = {
    "thumbnail": thumbnailer
}

conf["derives"] = {
    "thumbnail": [
        {"width": 1920},
        {"width": 1280},
        {"width": 900},
        {"width": 500}
    ]
}

# ------------------------------------------------------------------------------
# Language-specific configuration
#

# conf["viur.languageMethod"] = "url"
# conf["viur.availableLanguages"] = ["en", "de"]

# ------------------------------------------------------------------------------
# ViUR admin tool specific configurations
#

conf["admin.vi.name"] = "viurtest2"

# ------------------------------------------------------------------------------
# Email configuration
#

conf["viur.email.sendInBlue.apiKey"] = "xkeysib-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
conf["viur.email.transportClass"] = email.EmailTransportSendInBlue
# conf["viur.email.senderOverride"] = "mail@viur.dev"

# Email debugging config
# conf["viur.email.sendFromLocalDevelopmentServer"] = True  # enable sending emails from local development server
# conf["viur.email.recipientOverride"] = ["debug@viur.dev"]  # send all emails to this recipient

# ------------------------------------------------------------------------------
# Content Security Policy (CSP)
#

securityheaders.addCspRule("object-src", "none", "enforce")
securityheaders.addCspRule("style-src", "fonts.googleapis.com", "enforce")
securityheaders.addCspRule("style-src", "unsafe-inline", "enforce")
securityheaders.addCspRule("script-src", "apis.google.com", "enforce")
securityheaders.addCspRule("connect-src", "data:", "enforce")

conf["viur.security.contentSecurityPolicy"] = {}

# GitHub Buttons
#securityheaders.addCspRule("style-src", "unsafe-inline", "enforce")  # yes, GitHub buttons need this...
#securityheaders.addCspRule("script-src", "buttons.github.io", "enforce")
#securityheaders.addCspRule("connect-src", "api.github.com", "enforce")
# Enable this if you want to use the captcha, but not unsafe-inline:
# securityheaders.addCspRule("script-src", "sha256-TLq3i7CjxmHUoz+BrQ6w5D2+hv35BEkew240zhZ0uvA=", "enforce")

# ------------------------------------------------------------------------------
# Server startup
#


securityheaders.setXFrameOptions("off")

if conf["viur.instance.is_dev_server"]:
    from viur.datastore.config import conf as db_conf

    db_conf["traceQueries"] = True
    "Whitelist vueJs Frontend server"
    conf["viur.security.enableCORP"] = "cross-origin"


    def preprocessRequestHandler(path):
        request = current.request.get()
        referer = request.request.referer
        if referer and referer in ["http://localhost:8081/", "http://localhost:8082/"]:
            referer = request.request.referer[:-1]
            request.response.headers["Access-Control-Allow-Origin"] = referer

        request.response.headers["Access-Control-Allow-Credentials"] = "true"
        return path


    conf["viur.requestPreprocessor"] = preprocessRequestHandler

import modules
import render

app = core.setup(modules, render)


if conf["viur.instance.is_dev_server"]:
    logging.debug("==========================SERVER IS UP AND READY=================================")
    logging.debug(f"==========================USING CORE {core.version.__version__}==================================")
