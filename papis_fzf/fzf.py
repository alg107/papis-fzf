import functools
import sys
import os
#import dmenu
from pyfzf.pyfzf import FzfPrompt
from picker import picker as picker2

import papis.pick
import papis.format


#_fzf_pick = lambda x: FzfPrompt().prompt(x)[0]
_fzf_pick = lambda x: picker2(x)


def pick(options):
    cols = os.popen('tput cols', 'r').read().strip()
    cols = int(cols)
    #ts = cols-4-20-9
    ts = cols-6
    fmt = f'{{doc[year]:<4}} : {{doc[author]:<{ts-1}.{ts-1}}} \n    | {{doc[title]:<{ts-2}.{ts-2}}}'

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
