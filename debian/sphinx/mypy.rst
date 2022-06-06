====
mypy
====

SYNOPSIS
========

**mypy** [-h] [-v] [-V] [-m `MODULE`] [-p `PACKAGE`] [-c `PROGRAM_TEXT`] [`OPTIONS`...] [`FILES` ...]

DESCRIPTION
===========

Mypy is a static type checker for Python 3 and Python 2.7. If you sprinkle
your code with type annotations, mypy can type check your code and find
common bugs. As mypy is a static analyzer, or a lint-like tool, the type
annotations are just hints for mypy and don’t interfere when running
your program. You run your program with a standard Python interpreter,
and the annotations are treated effectively as comments.

Using the Python 3 function annotation syntax (using the PEP 484 notation)
or a comment-based annotation syntax for Python 2 code, you will be
able to efficiently annotate your code and use mypy to check the code
for common errors. Mypy has a powerful and easy-to-use type system with
modern features such as type inference, generics, callable types, tuple
types, union types, and structural subtyping.

Mypy is invoked with the paths the user needs to check::

$ mypy foo.py bar.py some_directory

The directories are checked recursively to find Python source files.

.. role:: ref
.. include:: mypy_options.rst

ENVIRONMENT
===========

**MYPYPATH**
   Additional module search path entries. The format is the same as the shell's `$PATH`: one or more directory pathnames separated by colons.

SEE ALSO
========

**dmypy**\(1)

Full documentation is available online at: http://mypy.readthedocs.io/en/latest/getting_started.html
or locally at: `/usr/share/doc/mypy/html <file:///usr/share/doc/mypy/html>`__ (requires `mypy-doc` package).
