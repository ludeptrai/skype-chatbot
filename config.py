#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

class DefaultConfig:
    """ Bot Configuration """

    PORT = 8080
    APP_ID = os.environ.get("MicrosoftAppId", "5ea3f2e9-3f5a-40db-a95b-bcdb73c6f86f")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "Yr5j_I8tYKRj:R8BVdtQ8EcImZBUg].f")
