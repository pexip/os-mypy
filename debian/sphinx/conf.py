# -*- coding: utf-8 -*-
project = 'Mypy'
author = 'Jukka Lehtosalo and contributors'
master_doc = 'index'
source_suffix = '.rst'

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('mypy', 'mypy',
     u'Optional static typing for Python',
     [author], 1),
    ('dmypy', 'dmypy',
     u'mypy daemon mode client',
     [author], 1),
    ('stubgen', 'stubgen',
     u'Generate draft type hint stubs for Python modules',
     [author], 1)
]
