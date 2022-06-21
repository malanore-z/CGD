import logging
import os
import subprocess

import zcommons as zc

from cgd import utils
from cgd.compile import Compiler
from cgd.generate import Generator


logger = logging.getLogger("cgd.diff")


class Diff(object):

    def __init__(self, sources, mode, data,
                 gen_path=None, gen_cls=None, std_src=None, std_lang=None, std_args=None, std_bin=None,
                 fc_path=None, fc_cls=None, rand_round=50, use_stdout=False, fail_fast=False, timeout=None):
        super(Diff, self).__init__()
        self.sources = sources
        self.mode = mode
        self.data = data

        self.gen_path = gen_path
        self.gen_cls = gen_cls
        self.std_src = std_src
        self.std_lang = std_lang
        self.std_args = std_args
        self.std_bin = std_bin

        self.fc_path = fc_path
        self.fc_cls = fc_cls
        self.rand_round = rand_round
        self.use_stdout = use_stdout
        self.fail_fast = fail_fast

        self.timeout = utils.first_not_none(timeout, utils.Global.timeout)

        self.__compilers = self.__compile_sources()

    def diff(self):
        try:
            logger.info(f"Compare sources in {self.mode} mode")
            self._diff()
        except Exception as e:
            logger.error(str(e))

    def _diff(self):
        fc_cls = zc.module.import_object(self.fc_cls, path=self.fc_path)
        self.__check_fc_cls(fc_cls)

        fc_dir = os.path.join(utils.Global.tmp_dir, "fc")
        os.makedirs(fc_dir, exist_ok=True)
        if self.mode == "std":
            if not self.data or not os.path.exists(self.data):
                raise ValueError(f"data path cannot be empty")
            for i in range(1, 10000):
                in_path, out_path = f"{self.data}/{i}.in", f"{self.data}/{i}.out"
                if not os.path.exists(in_path):
                    break
                logger.debug(f"Diff round #{i}")
                if not self.__execute_sources(fc_cls, in_path, out_path):
                    return
        elif self.mode == "rand":
            self.fail_fast = True
            gen = Generator("rand", os.path.join(fc_dir), gen_path=self.gen_path, gen_cls=self.gen_cls,
                            std_src=self.std_src, std_args=self.std_args, std_lang=self.std_lang, std_bin=self.std_bin,
                            timeout=self.timeout)
            in_path, out_path = os.path.join(fc_dir, "rand.in"), os.path.join(fc_dir, "rand.out")
            for i in range(self.rand_round):
                logger.info(f"Running round #{i+1}")
                gen.generate()
                if not self.__execute_sources(fc_cls, in_path, out_path):
                    return
        else:
            raise ValueError(f"Unsupported mode {self.mode}")

    def __execute_sources(self, fc_cls, in_path, out_path):
        fc_dir = os.path.join(utils.Global.tmp_dir, "fc")
        for idx, src in enumerate(self.sources):
            logger.debug(f"Running {src}")
            tmp_out_path = os.path.join(fc_dir, f"{idx}.out")
            if not self.__compilers[idx].executor.execute(in_path, tmp_out_path):
                return False
            if idx == 0:
                if self.use_stdout:
                    if not self._fc(fc_cls,
                                    out_path,
                                    tmp_out_path):
                        logger.error(
                            f"{zc.FORE_RED}FAILED{zc.FORE_RESET}: Comparison between stdout and {self.sources[idx]}")
                        if self.fail_fast:
                            return False
                    else:
                        logger.info(
                            f"{zc.FORE_GREEN}PASSED{zc.FORE_RESET}: Comparison between stdout and {self.sources[idx]}")
            else:
                if not self._fc(fc_cls,
                                os.path.join(fc_dir, f"{idx - 1}.out"),
                                tmp_out_path):
                    logger.error(
                        f"{zc.FORE_RED}FAILED{zc.FORE_RESET}: Comparison between {self.sources[idx - 1]} and {self.sources[idx]}")
                    if self.fail_fast:
                        return False
                else:
                    logger.info(
                        f"{zc.FORE_GREEN}PASSED{zc.FORE_RESET}: Comparison between {self.sources[idx - 1]} and {self.sources[idx]}")
        return True

    def __compile_sources(self):
        ret = []
        dst = os.path.join(utils.Global.tmp_dir, "bin")
        for src in self.sources:
            dst_name = utils.rand_token()
            c = Compiler(src, dst=dst, dst_name=dst_name)
            c.compile()
            ret.append(c)
        return ret

    def __check_fc_cls(self, fc_cls):
        if fc_cls is None:
            raise ValueError(f"cannot import {self.fc_cls}")
        if not callable(fc_cls):
            raise ValueError(f"{self.fc_cls} is not callable")

    def _fc(self, fc_cls, out_l, out_r):
        fc = fc_cls(out_l, out_r)
        if not fc.compare():
            logger.info(fc.detail())
            return False
        else:
            return True
