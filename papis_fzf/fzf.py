import functools
#import dmenu
from pyfzf.pyfzf import FzfPrompt

import papis.pick
import papis.format
import os

cols = os.popen('tput cols', 'r').read().strip()
cols = int(cols)

_fzf_pick = lambda x: FzfPrompt().prompt(x)[0]


def pick(options):

    ts = cols-4-20-9
    fmt = f'{{doc[author]:<20.20}} | {{doc[title]:<{ts}.{ts}}} | {{doc[year]:<4}}'

    if len(options) == 1:
        index = 0
    elif len(options) == 0:
        return ''
    else:

        def header_filter(x):
            return papis.format.format(fmt, x)

        headers = [header_filter(o) for o in options]
        header = _fzf_pick(headers)
        if not header:
            return None
        index = headers.index(header)

    return options[index]


class Picker(papis.pick.Picker):

    def __call__(self,
                 items,
                 header_filter,
                 match_filter,
                 default_index: int = 0):
        return [pick(items)]


def input(prompt=''):
    return _fzf_pick([], prompt=prompt)
