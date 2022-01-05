from types import FrameType, TracebackType
from typing import IO, List, Optional, Tuple, Type

_PT = Tuple[str, int, str, Optional[str]]

def print_tb(tb: TracebackType | None, limit: int | None = ..., file: IO[str] | None = ...) -> None: ...
def print_exception(
    etype: Type[BaseException] | None,
    value: BaseException | None,
    tb: TracebackType | None,
    limit: int | None = ...,
    file: IO[str] | None = ...,
) -> None: ...
def print_exc(limit: int | None = ..., file: IO[str] | None = ...) -> None: ...
def print_last(limit: int | None = ..., file: IO[str] | None = ...) -> None: ...
def print_stack(f: FrameType | None = ..., limit: int | None = ..., file: IO[str] | None = ...) -> None: ...
def extract_tb(tb: TracebackType | None, limit: int | None = ...) -> List[_PT]: ...
def extract_stack(f: FrameType | None = ..., limit: int | None = ...) -> List[_PT]: ...
def format_list(extracted_list: List[_PT]) -> List[str]: ...
def format_exception_only(etype: Type[BaseException] | None, value: BaseException | None) -> List[str]: ...
def format_exception(
    etype: Type[BaseException] | None, value: BaseException | None, tb: TracebackType | None, limit: int | None = ...
) -> List[str]: ...
def format_exc(limit: int | None = ...) -> str: ...
def format_tb(tb: TracebackType | None, limit: int | None = ...) -> List[str]: ...
def format_stack(f: FrameType | None = ..., limit: int | None = ...) -> List[str]: ...
def tb_lineno(tb: TracebackType) -> int: ...
