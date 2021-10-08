=======
stubgen
=======

SYNOPSIS
========

**stubgen** [-h] [-py2] [-m `MODULE`] [-p `PACKAGE`] [`OPTIONS`...] [`FILES`...]

DESCRIPTION
===========

Mypy is a static type checker for Python 3 and Python 2.7. Mypy includes
the `stubgen` tool that can automatically generate stub files (`.pyi`
files) for Python modules and C extension modules.

A stub file (see PEP 484) contains only type hints for the public
interface of a module, with empty function bodies. Mypy can use a stub
file instead of the real implementation to provide type information for
the module. They are useful for third-party modules whose authors have
not yet added type hints (and when no stubs are available in typeshed)
and C extension modules (which mypy can’t directly process).

Stubgen generates *draft* stubs. The auto-generated stub files often require some manual updates, and most types will default to `Any`. The stubs will be much more useful if you add more precise type annotations, at least for the most commonly used functionality.

OPTIONS
=======

.. role:: ref
.. include:: stubgen_options.rst

ENVIRONMENT
===========

**MYPYPATH**
   Additional module search path entries. The format is the same as the shell's `$PATH`: one or more directory pathnames separated by colons.

SEE ALSO
========

**mypy**\(1)

Full documentation is available online at: https://mypy.readthedocs.io/en/latest/stubgen.html
or locally at: `/usr/share/doc/mypy/html <file:///usr/share/doc/mypy/html>`__ (requires `mypy-doc` package).
