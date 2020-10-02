import enum
import os
import sys
import warnings
import tempfile
from typing import Optional

import win32gui

__version__ = '1.1.0'
__author__ = 'Gaming32'


class Mode(enum.Enum):
    SelectionBox = 'p'
    ConfigurationBox = 'c'
    Fullscreen = 's'


class Screensaver:
    mode: Mode
    handle: Optional[int]

    def __init__(self, mode=Mode.Fullscreen, specified_handle=None) -> None:
        self.mode = mode
        self.specified_handle = specified_handle
        self.handle = None

    @staticmethod
    def parse_cmdline(argv=None):
        if argv is None:
            argv = sys.argv[1:]
        mode = Mode.Fullscreen
        handle = None
        for arg in argv:
            arg = arg.strip('/')
            full_arg = arg.split(':')
            mode = Mode(full_arg[0])
            if len(full_arg) > 1:
                handle = int(full_arg[1])
        return Screensaver(mode, handle)

    def set_handle(self, handle: int):
        warnings.warn('Please assign Screensaver.handle directly instead of calling Screensaver.set_handle', DeprecationWarning)
        self.handle = handle

    def recreate_cmdline(self) -> list:
        res = f'/{self.mode.value}'
        if self.specified_handle is not None:
            res += f':{self.specified_handle}'
        return [res]

    def __repr__(self) -> str:
        return f'{self.__class__.__qualname__}.parse_cmdline({self.recreate_cmdline()!r})'

    def reparent(self):
        if self.specified_handle is None:
            return
        if self.handle is None:
            raise ValueError('no window specified to reparent')
        win32gui.SetParent(self.handle, self.specified_handle)


default_logfile = tempfile.mktemp('.log', 'screensaver_')
def parse_cmdline(argv=None, handle=None, logfile=default_logfile) -> Screensaver:
    try:
        scr = Screensaver.parse_cmdline(argv)
    except ValueError:
        err_argv = sys.argv[1:] if argv is None else argv
        raise ValueError(f'Incorrect command line arguments passed: {err_argv}') from None
    scr.handle = handle
    if logfile is not None:
        redirect_stdout(logfile)
    return scr


def redirect_stdout(logfile=None):
    if logfile is None:
        sys.stdout = sys.__stdout__
        return
    sys.stdout = open(logfile, 'w')


if __name__ == '__main__':
    print(parse_cmdline())
