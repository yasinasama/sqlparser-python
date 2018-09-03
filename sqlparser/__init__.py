# -*- coding: utf-8 -*-

import json

from .grammar import parse_handle

def parse(sql):
    try:
        return json.dumps(parse_handle(sql))
    except Exception:
        raise