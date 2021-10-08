=====
dmypy
=====

SYNOPSIS
========

**dmypy** [OPTIONS...] `COMMAND`] [COMMAND OPTIONS ...]

DESCRIPTION
===========

Mypy can run as a long-running daemon (server) process allowing to perform
type checking much faster, since program state cached from previous runs
is kept in memory and doesn’t have to be read from the file system
on each run. The server also uses finer-grained dependency tracking to
reduce the amount of work that needs to be done.

If you have a large codebase to check, running mypy using the mypy daemon
can be 10 or more times faster than the regular command-line **mypy** tool,
especially if your workflow involves running mypy repeatedly after
small edits – which is often a good idea, as this way you’ll find
errors sooner.

Dmypy is a command-line client to send type-checking requests to the server.

COMMANDS
========

start [--log-file `FILE`] [--timeout `TIMEOUT`] `ARGS`...
*********************************************************

Start a mypy daemon.

Runs a new mypy daemon, passing regular mypy flags to it.
If `--log-file` is used, directs daemon stdout/stderr to `FILE`.
`--timeout` specifies the server shutdown timeout in seconds.

stop
****

Stop a mypy daemon.

Politely asks the currently running mypy daemon to go away.

kill
****

Kill a mypy daemon.

Kills the process of the currently running mypy daemon.

restart [--log-file `FILE`] [--timeout `TIMEOUT`] `ARGS`...
***********************************************************

Restart a mypy daemon.

Stops the existing and then runs a new mypy daemon, passing regular mypy flags to it.
If `--log-file` is used, directs daemon stdout/stderr to `FILE`.
`--timeout` specifies the server shutdown timeout in seconds.

status [-v]
***********

Show a mypy daemon status.

If `-v` or `--verbose` is used, prints detailed status.

daemon [--timeout `TIMEOUT`] `ARGS`...
**************************************

Run a mypy daemon in the foreground, passing regular mypy flags to it.

`--timeout` specifies the server shutdown timeout in seconds.

check [-v] [--junit-xml `JUNIT_XML`] [--perf-stats-file `PERF_STATS_FILE`] `FILE` [`FILE` ...]
**********************************************************************************************

Check some files.

Tell the currently running mypy daemon to check some files. This requires the daemon to already be running.

-v, --verbose                       Print detailed status
--junit-xml JUNIT_XML               Write junit.xml to the given file
--perf-stats-file PERF_STATS_FILE   Write telemetry information to the given file

recheck [-v] [--junit-xml `JUNIT_XML`] [--perf-stats-file `PERF_STATS_FILE`] [--update `FILE` [`FILE` ...]] [--remove `FILE` [`FILE` ...]]
******************************************************************************************************************************************

Re-check the previous list of files, with optional modifications. This requires the daemon to already be running.

-v, --verbose                       Print detailed status
--junit-xml JUNIT_XML               Write junit.xml to the given file
--perf-stats-file PERF_STATS_FILE   Write telemetry information to the given file

run [-v] [--junit-xml `JUNIT_XML`] [--perf-stats-file `PERF_STATS_FILE`] [--timeout `TIMEOUT`] [--log-file `FILE`] `ARGS`...
****************************************************************************************************************************

Check some files, (re)starting the daemon if necessary.

-v, --verbose                       Print detailed status
--junit-xml JUNIT_XML               Write junit.xml to the given file
--perf-stats-file PERF_STATS_FILE   Write telemetry information to the given file
--timeout TIMEOUT                   Server shutdown timeout (in seconds)
--log-file FILE                     Direct daemon stdout/stderr to `FILE`

hang
****

Hang for 100 seconds.

OPTIONS
=======

``-h``, ``--help``
   Show a help message and exit.

``--status-file`` `STATUS_FILE`
   Status file to retrieve daemon details to.

``-V``, ``--version``
   Show program’s version number and exit.

SEE ALSO
========

**mypy**\(1)

Full documentation is available online at: https://mypy.readthedocs.io/en/latest/mypy_daemon.html
or locally at: `/usr/share/doc/mypy/html <file:///usr/share/doc/mypy/html>`__ (requires `mypy-doc` package).
