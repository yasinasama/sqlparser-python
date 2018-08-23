# -*- coding: utf-8 -*-

from .grammar import parse_handle

def parse(sql):
    try:
        return parse_handle(sql)
    except Exception as e:
        raise