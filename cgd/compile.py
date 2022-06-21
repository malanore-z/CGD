import logging
import os

import zcommons as zc

from cgd import utils
from cgd.constants import Lang, DEFAULT_ARGS
from cgd.execute import Executor


logger = logging.getLogger("cgd.compile")


class Compiler(object):

    def __init__(self, src, dst=None, dst_name=None, lang=None, args=None, timeout=None):
        super(Compiler, self).__init__()
        self.src = utils.format_path(src)
        self.dst = utils.format_path(dst)
        if self.dst:
            os.makedirs(self.dst, exist_ok=True)
        self.dst_name = dst_name
        self.lang = utils.parse_lang(self.src) if lang is None else utils.format_lang(lang)
        self.args = args if args else DEFAULT_ARGS.get(self.lang, [])
        self.timeout = utils.first_not_none(timeout, utils.Global.timeout)
        self.__exe = None
        self.__dst_path = None

    @property
    def dst_path(self):
        return self.__dst_path

    @property
    def executor(self):
        return self.__exe

    def compile(self):
        try:
            logger.info(f"Compile {self.src}")
            ret = self._compile()
            if not self.__exe:
                self.__dst_path = self.__dst(as_arg=False)
                self.__exe = Executor(self.__dst_path, self.lang)
            return ret
        except Exception as e:
            logger.error(str(e))

    def _compile(self):
        cmd = self.__parse_cmd()
        logger.debug(f"Compile command: {cmd}")
        tmer = zc.Timer(unit="ms")
        tmer.start()
        ret, returncode = utils.run_subprocess(cmd, self.timeout, None, None, None, logger)
        tmer.stop()
        if ret == 0:
            if returncode == 0:
                logger.info(f"Compiled successfully, it took {tmer.elapsed()[0]}ms")
            else:
                logger.info(f"Compilation failed. return code is {returncode}.")
        elif ret == 1:
            logger.error(f"Compilation timeout.")
        else:
            logger.error(f"Unknown error occurred when compile.")
        return ret == 0 and returncode == 0

    def __parse_cmd(self):
        cmd = []
        src = self.src
        dst = self.__dst(as_arg=True)
        if self.lang == Lang.C or self.lang == Lang.CPP:
            cmd.append("gcc" if self.lang == Lang.C else "g++")
            cmd.append(self.src)
            if self.args:
                cmd.extend(self.args)
            cmd.append("-o")
            cmd.append(dst)
        elif self.lang == Lang.JAVA:
            cmd.append("javac")
            if self.args:
                cmd.extend(self.args)
            cmd.append(src)
            cmd.append("-d")
            cmd.append(dst)
        elif self.lang == Lang.PY:
            if utils.is_win32():
                cmd.extend(["cmd", "/c", "copy"])
            else:
                cmd.extend(["cp"])
            cmd.append(src)
            cmd.append(dst)
        else:
            raise ValueError(f"Illegal lang {self.lang}")
        return cmd

    def __dst(self, as_arg):
        src_dir = os.path.dirname(self.src)
        src_name = os.path.basename(self.src)
        dst_dir = utils.first_not_none(self.dst, src_dir)
        dst_name = utils.first_not_none(self.dst_name, src_name)
        if self.lang == Lang.C or self.lang == Lang.CPP:
            if dst_name.endswith(".c"):
                dst_name = dst_name[:-2]
            elif dst_name.endswith(".cpp"):
                dst_name = dst_name[:-4]
            return utils.format_path(os.path.join(dst_dir, dst_name))
        elif self.lang == Lang.JAVA:
            if as_arg:
                return dst_dir
            else:
                dst_name = src_name
                if dst_name.endswith(".java"):
                    dst_name = dst_name[:-5]
                if not dst_name.endswith(".class"):
                    dst_name += ".class"
                return utils.format_path(os.path.join(dst_dir, dst_name))
        elif self.lang == Lang.PY:
            if not dst_name.endswith(".py"):
                dst_name += ".py"
            return utils.format_path(os.path.join(dst_dir, dst_name))
        else:
            raise ValueError(f"Illegal lang {self.lang}")
