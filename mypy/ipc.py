"""Cross platform abstractions for inter-process communication

On Unix, this uses AF_UNIX sockets.
On Windows, this uses NamedPipes.
"""

from __future__ import annotations

import base64
import os
import shutil
import sys
import tempfile
from types import TracebackType
from typing import Callable
from typing_extensions import Final

if sys.platform == "win32":
    # This may be private, but it is needed for IPC on Windows, and is basically stable
    import ctypes

    import _winapi

    _IPCHandle = int

    kernel32 = ctypes.windll.kernel32
    DisconnectNamedPipe: Callable[[_IPCHandle], int] = kernel32.DisconnectNamedPipe
    FlushFileBuffers: Callable[[_IPCHandle], int] = kernel32.FlushFileBuffers
else:
    import socket

    _IPCHandle = socket.socket


class IPCException(Exception):
    """Exception for IPC issues."""


class IPCBase:
    """Base class for communication between the dmypy client and server.

    This contains logic shared between the client and server, such as reading
    and writing.
    """

    connection: _IPCHandle

    def __init__(self, name: str, timeout: float | None) -> None:
        self.name = name
        self.timeout = timeout

    def read(self, size: int = 100000) -> bytes:
        """Read bytes from an IPC connection until its empty."""
        bdata = bytearray()
        if sys.platform == "win32":
            while True:
                ov, err = _winapi.ReadFile(self.connection, size, overlapped=True)
                try:
                    if err == _winapi.ERROR_IO_PENDING:
                        timeout = int(self.timeout * 1000) if self.timeout else _winapi.INFINITE
                        res = _winapi.WaitForSingleObject(ov.event, timeout)
                        if res != _winapi.WAIT_OBJECT_0:
                            raise IPCException(f"Bad result from I/O wait: {res}")
                except BaseException:
                    ov.cancel()
                    raise
                _, err = ov.GetOverlappedResult(True)
                more = ov.getbuffer()
                if more:
                    bdata.extend(more)
                if err == 0:
                    # we are done!
                    break
                elif err == _winapi.ERROR_MORE_DATA:
                    # read again
                    continue
                elif err == _winapi.ERROR_OPERATION_ABORTED:
                    raise IPCException("ReadFile operation aborted.")
        else:
            while True:
                more = self.connection.recv(size)
                if not more:
                    break
                bdata.extend(more)
        return bytes(bdata)

    def write(self, data: bytes) -> None:
        """Write bytes to an IPC connection."""
        if sys.platform == "win32":
            try:
                ov, err = _winapi.WriteFile(self.connection, data, overlapped=True)
                try:
                    if err == _winapi.ERROR_IO_PENDING:
                        timeout = int(self.timeout * 1000) if self.timeout else _winapi.INFINITE
                        res = _winapi.WaitForSingleObject(ov.event, timeout)
                        if res != _winapi.WAIT_OBJECT_0:
                            raise IPCException(f"Bad result from I/O wait: {res}")
                    elif err != 0:
                        raise IPCException(f"Failed writing to pipe with error: {err}")
                except BaseException:
                    ov.cancel()
                    raise
                bytes_written, err = ov.GetOverlappedResult(True)
                assert err == 0, err
                assert bytes_written == len(data)
            except OSError as e:
                raise IPCException(f"Failed to write with error: {e.winerror}") from e
        else:
            self.connection.sendall(data)
            self.connection.shutdown(socket.SHUT_WR)

    def close(self) -> None:
        if sys.platform == "win32":
            if self.connection != _winapi.NULL:
                _winapi.CloseHandle(self.connection)
        else:
            self.connection.close()


class IPCClient(IPCBase):
    """The client side of an IPC connection."""

    def __init__(self, name: str, timeout: float | None) -> None:
        super().__init__(name, timeout)
        if sys.platform == "win32":
            timeout = int(self.timeout * 1000) if self.timeout else _winapi.NMPWAIT_WAIT_FOREVER
            try:
                _winapi.WaitNamedPipe(self.name, timeout)
            except FileNotFoundError as e:
                raise IPCException(f"The NamedPipe at {self.name} was not found.") from e
            except OSError as e:
                if e.winerror == _winapi.ERROR_SEM_TIMEOUT:
                    raise IPCException("Timed out waiting for connection.") from e
                else:
                    raise
            try:
                self.connection = _winapi.CreateFile(
                    self.name,
                    _winapi.GENERIC_READ | _winapi.GENERIC_WRITE,
                    0,
                    _winapi.NULL,
                    _winapi.OPEN_EXISTING,
                    _winapi.FILE_FLAG_OVERLAPPED,
                    _winapi.NULL,
                )
            except OSError as e:
                if e.winerror == _winapi.ERROR_PIPE_BUSY:
                    raise IPCException("The connection is busy.") from e
                else:
                    raise
            _winapi.SetNamedPipeHandleState(
                self.connection, _winapi.PIPE_READMODE_MESSAGE, None, None
            )
        else:
            self.connection = socket.socket(socket.AF_UNIX)
            self.connection.settimeout(timeout)
            self.connection.connect(name)

    def __enter__(self) -> IPCClient:
        return self

    def __exit__(
        self,
        exc_ty: type[BaseException] | None = None,
        exc_val: BaseException | None = None,
        exc_tb: TracebackType | None = None,
    ) -> None:
        self.close()


class IPCServer(IPCBase):

    BUFFER_SIZE: Final = 2**16

    def __init__(self, name: str, timeout: float | None = None) -> None:
        if sys.platform == "win32":
            name = r"\\.\pipe\{}-{}.pipe".format(
                name, base64.urlsafe_b64encode(os.urandom(6)).decode()
            )
        else:
            name = f"{name}.sock"
        super().__init__(name, timeout)
        if sys.platform == "win32":
            self.connection = _winapi.CreateNamedPipe(
                self.name,
                _winapi.PIPE_ACCESS_DUPLEX
                | _winapi.FILE_FLAG_FIRST_PIPE_INSTANCE
                | _winapi.FILE_FLAG_OVERLAPPED,
                _winapi.PIPE_READMODE_MESSAGE
                | _winapi.PIPE_TYPE_MESSAGE
                | _winapi.PIPE_WAIT
                | 0x8,  # PIPE_REJECT_REMOTE_CLIENTS
                1,  # one instance
                self.BUFFER_SIZE,
                self.BUFFER_SIZE,
                _winapi.NMPWAIT_WAIT_FOREVER,
                0,  # Use default security descriptor
            )
            if self.connection == -1:  # INVALID_HANDLE_VALUE
                err = _winapi.GetLastError()
                raise IPCException(f"Invalid handle to pipe: {err}")
        else:
            self.sock_directory = tempfile.mkdtemp()
            sockfile = os.path.join(self.sock_directory, self.name)
            self.sock = socket.socket(socket.AF_UNIX)
            self.sock.bind(sockfile)
            self.sock.listen(1)
            if timeout is not None:
                self.sock.settimeout(timeout)

    def __enter__(self) -> IPCServer:
        if sys.platform == "win32":
            # NOTE: It is theoretically possible that this will hang forever if the
            # client never connects, though this can be "solved" by killing the server
            try:
                ov = _winapi.ConnectNamedPipe(self.connection, overlapped=True)
            except OSError as e:
                # Don't raise if the client already exists, or the client already connected
                if e.winerror not in (_winapi.ERROR_PIPE_CONNECTED, _winapi.ERROR_NO_DATA):
                    raise
            else:
                try:
                    timeout = int(self.timeout * 1000) if self.timeout else _winapi.INFINITE
                    res = _winapi.WaitForSingleObject(ov.event, timeout)
                    assert res == _winapi.WAIT_OBJECT_0
                except BaseException:
                    ov.cancel()
                    _winapi.CloseHandle(self.connection)
                    raise
                _, err = ov.GetOverlappedResult(True)
                assert err == 0
        else:
            try:
                self.connection, _ = self.sock.accept()
            except socket.timeout as e:
                raise IPCException("The socket timed out") from e
        return self

    def __exit__(
        self,
        exc_ty: type[BaseException] | None = None,
        exc_val: BaseException | None = None,
        exc_tb: TracebackType | None = None,
    ) -> None:
        if sys.platform == "win32":
            try:
                # Wait for the client to finish reading the last write before disconnecting
                if not FlushFileBuffers(self.connection):
                    raise IPCException(
                        "Failed to flush NamedPipe buffer, maybe the client hung up?"
                    )
            finally:
                DisconnectNamedPipe(self.connection)
        else:
            self.close()

    def cleanup(self) -> None:
        if sys.platform == "win32":
            self.close()
        else:
            shutil.rmtree(self.sock_directory)

    @property
    def connection_name(self) -> str:
        if sys.platform == "win32":
            return self.name
        else:
            name = self.sock.getsockname()
            assert isinstance(name, str)
            return name
