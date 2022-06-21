import abc
import typing


class BaseSample(object):

    def __getitem__(self, item) -> typing.Generator:
        pass

    def __len__(self) -> int:
        pass

    def write_to(self, f):
        if isinstance(f, str):
            with open(f, "w") as real_f:
                self.__write_to(real_f)
        else:
            self.__write_to(f)

    def __write_to(self, f):
        for elems in self:
            first = True
            for e in elems:
                if not first:
                    f.write(' ')
                f.write(str(e))
                first = False
            f.write('\n')


class BaseGenerator(object):

    def __init__(self):
        super(BaseGenerator, self).__init__()
        self.fixed_samples: typing.List[typing.Tuple[BaseSample, BaseSample]] = []
        self.rand_args: typing.List[typing.Tuple[BaseSample, BaseSample]] = []

    def __getitem__(self, item) -> typing.Tuple[BaseSample, BaseSample]:
        if item < len(self.fixed_samples):
            return self.fixed_samples[item]
        else:
            item = item - len(self.fixed_samples)
            return self._generate(*self.rand_args[item])

    def __len__(self) -> int:
        return len(self.fixed_samples) + len(self.rand_args)

    @abc.abstractmethod
    def _generate(self, *args, **kwargs) -> typing.Tuple[BaseSample, BaseSample]:
        pass

    @abc.abstractmethod
    def rand(self, *args, **kwargs) -> typing.Tuple[BaseSample, BaseSample]:
        return self._generate(*args, **kwargs)
