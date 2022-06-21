import logging
import os
import typing

import zcommons as zc

from cgd import utils
from cgd.compile import Compiler
from cgd.execute import Executor
from cgd.data import *


logger = logging.getLogger("cgd.generate")


class Generator(object):

    def __init__(self, mode, output, gen_path=None, gen_cls=None,
                 std_src=None, std_lang=None, std_args=None, std_bin=None,
                 timeout=None):
        super(Generator, self).__init__()
        self.mode = mode
        self.output = output
        self.gen_path = gen_path
        self.gen_cls = gen_cls
        self.std_src = std_src
        self.std_lang = std_lang
        self.std_args = std_args
        self.std_bin = std_bin
        self.timeout = timeout

    def generate(self):
        try:
            logger.info(f"Generate samples in {self.mode} mode")
            self._generate()
        except Exception as e:
            logger.error(str(e))

    def _generate(self):
        os.makedirs(self.output, exist_ok=True)
        gen_cls = zc.module.import_object(self.gen_cls, path=self.gen_path)
        self.__check_gen_cls(gen_cls)
        gen_obj = gen_cls()
        std_exe = self.__std_executor()
        tmer = zc.Timer(unit="ms")
        tmer.start()
        if self.mode == "std" or self.mode == "stdout":
            for i, sample in enumerate(gen_obj):
                logger.debug(f"Generated sample {i+1}, used {tmer.last_record()[0]}ms")
                in_path, out_path = f"{self.output}/{i + 1}.in", f"{self.output}/{i + 1}.out"
                in_sample, out_sample = self.__split_sample(sample)
                if in_sample is not None:
                    in_sample.write_to(in_path)
                else:
                    raise ValueError(f"Generated None sample input")
                if out_sample is not None:
                    out_sample.write_to(out_path)
                else:
                    if std_exe:
                        tmer.record()
                        std_exe.execute(in_path, out_path)
                        logger.debug(f"Generated sample output {i+1} in stdout mode, used {tmer.last_record()[0]}ms")
                tmer.record()
        elif self.mode == "rand":
            sample = gen_obj.rand()
            logger.debug(f"Generated rand sample, used {tmer.last_record()[0]}ms")
            in_path, out_path = f"{self.output}/rand.in", f"{self.output}/rand.out"
            in_sample, out_sample = self.__split_sample(sample)
            if in_sample is not None:
                in_sample.write_to(in_path)
            if out_sample is not None:
                out_sample.write_to(out_path)
        else:
            raise ValueError(f"Unsupported mode {self.mode}")
        tmer.stop()

    def __std_executor(self):
        if self.mode != "stdout":
            return None
        if self.std_bin:
            exe = Executor(self.std_bin, timeout=self.timeout)
            return exe
        if self.std_src:
            com = Compiler(self.std_src, dst=os.path.join(utils.Global.tmp_dir, "bin"), lang=self.std_lang,
                           args=self.std_args, timeout=self.timeout)
            com.compile()
            return com.executor
        raise ValueError(f"'std_bin' and 'std_src' argument cannot be both None in stdout mode")

    def __check_gen_cls(self, gen_cls):
        if gen_cls is None:
            raise ValueError(f"cannot import {self.gen_cls}")
        if not callable(gen_cls):
            raise ValueError(f"{self.gen_cls} is not callable")

    def __split_sample(self, sample) -> typing.Tuple[BaseSample, typing.Union[BaseSample, None]]:
        if isinstance(sample, BaseSample):
            return sample, None
        return sample[0], sample[1]