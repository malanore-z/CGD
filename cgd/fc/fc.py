__all__ = [
    "FC"
]

import abc


class FC(object):

    def __init__(self, src: str, dst: str):
        super(FC, self).__init__()
        self.src = src
        self.dst = dst
        self._src_line = ""
        self._dst_line = ""

    @abc.abstractmethod
    def compare(self) -> bool:
        pass

    def detail(self) -> str:
        if self._src_line == self._dst_line:
            return ""
        dash_num = max(80, len(self._src_line), len(self._dst_line)) + 2
        ret = [
            f"< {self._src_line[:80]}",
            "-" * dash_num,
            f"> {self._dst_line[:80]}"
        ]
        return "\n".join(ret)

    def __call__(self):
        return self.compare()

    def __repr__(self) -> str:
        return self.detail()
