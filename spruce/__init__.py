VERSION = {
    'major': 0,
    'minor': 0,
    'micro': 1,
    'releaselevel': 'final',
    'serial': 1,
}


def get_version(short=False):
    vers = ['%(major)i.%(minor)i' % VERSION, ]

    if VERSION['micro']:
        vers.append('.%(micro)i' % VERSION)
    if VERSION['releaselevel'] != 'final' and not short:
        vers.append('%(releaselevel)s%(serial)i' % VERSION)

    return ''.join(vers)

__version__ = get_version()
