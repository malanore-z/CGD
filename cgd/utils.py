import logging
import os
import random
import subprocess
from pathlib import WindowsPath, PosixPath

import zcommons as zc

from cgd.constants import Lang


__ext_2_lang = {
    "c": Lang.C,
    "cpp": Lang.CPP,
    "java": Lang.JAVA,
    "class": Lang.JAVA,
    "py": Lang.PY
}


def is_win32():
    return os.name == "nt"


def parse_lang(name):
    global __ext_2_lang
    if not name:
        return Lang.UNKNOWN
    name, _, ext = name.rpartition(".")
    if name:
        return __ext_2_lang.get(ext, Lang.UNKNOWN)
    else:
        return Lang.UNKNOWN


def format_lang(lang):
    if not lang:
        return Lang.UNKNOWN
    if isinstance(lang, str):
        return Lang(lang.lower())
    return Lang(lang)


def format_path(path):
    if not path:
        return path
    if is_win32():
        p = WindowsPath(os.path.abspath(path))
        return str(p)
    else:
        p = PosixPath(os.path.abspath(path))
        return str(p)


def setattr_if_none(obj, name, value):
    if getattr(obj, name, None) is None:
        setattr(obj, name, value)


def first_not_none(*args):
    for arg in args:
        if arg is not None:
            return arg
    return None


__token_choices = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"


def rand_token(length=8):
    global __token_choices
    return "".join(random.choices(__token_choices, k=length))


def run_subprocess(cmd, timeout, stdin, stdout, stderr, logger):
    if not logger.isEnabledFor(logging.DEBUG):
        if stdout is None:
            stdout = subprocess.PIPE
        if stderr is None:
            stderr = subprocess.PIPE
    tmer = zc.Timer(unit="ms")
    tmer.start()
    try:
        logger.debug(f"Run subprocess {cmd}")
        cp = subprocess.run(cmd, timeout=timeout/1000, stdin=stdin, stdout=stdout, stderr=stderr)
        logger.debug(f"Subprocess ends, return code is {cp.returncode}")
        return 0, cp.returncode
    except subprocess.TimeoutExpired:
        logger.error(f"Run subprocess {cmd} timeout expired")
        return 1, 0
    except Exception as e:
        logger.error(f"Unknown error occurred while the subprocess {cmd} running: {str(e)}")
        return 2, 0
    finally:
        tmer.stop()
        logger.debug(f"Subprocess ends, cost {tmer.elapsed()[0]}ms.")


class WorkdirContext(object):

    def __init__(self, workdir):
        super(WorkdirContext, self).__init__()
        self.__workdir = os.path.abspath(workdir) if workdir is not None else None
        self.__curdir = None

    def __enter__(self):
        if self.__workdir is not None:
            self.__curdir = os.path.abspath(os.curdir)
            os.chdir(self.__workdir)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__workdir is not None:
            os.chdir(self.__curdir)


class FileContext(object):

    def __init__(self, stdin, stdout, w_mode="w"):
        super(FileContext, self).__init__()
        self.__orig_stdin = stdin
        self.__orig_stdout = stdout
        self.__w_mode = w_mode
        self.__stdin_opened = False
        self.__stdout_opened = False
        self.__stdin = None
        self.__stdout = None

    @property
    def stdin(self):
        return self.__stdin

    @property
    def stdout(self):
        return self.__stdout

    def __enter__(self):
        if isinstance(self.__orig_stdin, str):
            self.__stdin = open(self.__orig_stdin)
            self.__stdin_opened = True
        else:
            self.__stdin = self.__orig_stdin
        if isinstance(self.__orig_stdout, str):
            self.__stdout = open(self.__orig_stdout, self.__w_mode)
            self.__stdout_opened = True
        else:
            self.__stdout = self.__orig_stdout
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__stdin is not None and self.__stdin_opened:
            self.__stdin.close()
            self.__stdin_opened = False
        if self.__stdout is not None and self.__stdout_opened:
            self.__stdout.close()
            self.__stdout_opened = False


class Global(object):

    tmp_dir = "tmp"
    timeout = 3000
