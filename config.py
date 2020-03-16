#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT =int(os.environ.get(“PORT”, 5000))
    # APP_ID = os.environ.get("MicrosoftAppId", "")
    # APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    APP_ID = os.environ.get("MicrosoftAppId", "5ea3f2e9-3f5a-40db-a95b-bcdb73c6f86f")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "rm0OPaHo0Xjmsv5IcHhY-=jftAYf3Z-]")
