# -*- coding: UTF-8 -*-

import re


def parse_word(content):
    container = {}
    result = re.finditer(r"\w+", content)
    for match in result:
        container[match.group()] = 0
    return "\n".join(list(container.keys()))
