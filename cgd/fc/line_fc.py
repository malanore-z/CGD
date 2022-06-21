__all__ = [
    "LineFC",
    "StrictLineFC",
    "IgnoreAllBlankLineFC",
    "IgnoreBEBlankLineFC",
    "IgnoreAllBlankLineAndBESpaceFC"
]


from .fc import FC


class LineFC(FC):

    def __init__(self, src: str, dst: str, ignore=0):
        """

        :param src:
        :param dst:
        :param ignore: 0 - strict, 1 - ignore blank line at the beginning and end,
                        2 - ignore all blank line,
                        3 - ignore all blank line and space at the beginning and end of a line
        """
        super(LineFC, self).__init__(src, dst)
        self.ignore = ignore

    def compare(self) -> bool:
        with open(self.src, "r") as src_f, open(self.dst, "r") as dst_f:
            src_lines = self.__remove_end_lf(src_f.readlines())
            dst_lines = self.__remove_end_lf(dst_f.readlines())
        if self.ignore > 0:
            src_lines = self.__remove_be_blank_line(src_lines)
            dst_lines = self.__remove_be_blank_line(dst_lines)
        if self.ignore > 1:
            src_lines = self.__remove_be_blank_line(src_lines)
            dst_lines = self.__remove_all_blank_line(dst_lines)
        if self.ignore > 2:
            src_lines = self.__remove_be_whitespace(src_lines)
            dst_lines = self.__remove_be_whitespace(dst_lines)

        min_len = min(len(src_lines), len(dst_lines))
        for i in range(min_len):
            if src_lines[i] != dst_lines[i]:
                self._src_line = src_lines[i]
                self._dst_line = dst_lines[i]
                return False

        if len(src_lines) > min_len:
            self._src_line = src_lines[min_len]
            self._dst_line = "EOF"
            return False

        if len(dst_lines) > min_len:
            self._src_line = "EOF"
            self._dst_line = dst_lines[min_len]
            return False

        return True

    def __remove_end_lf(self, lines):
        for i in range(len(lines)):
            if lines[i][-1] == '\n':
                lines[i] = lines[i][:-1]
        return lines

    def __remove_be_blank_line(self, lines):
        sp, ep = 0, 0
        for i in range(len(lines)):
            if lines[i] == "" or lines[i] == "\n":
                sp = i
            else:
                break
        for i in range(len(lines) - 1, -1, -1):
            if lines[i] == "" or lines[i] == "\n":
                ep = i
            else:
                break

        return lines[sp: ep + 1]

    def __remove_all_blank_line(self, lines):
        ret = []
        for line in lines:
            if line != "" and line != "\n":
                ret.append(line)
        return ret

    def __remove_be_whitespace(self, lines):
        ret = []
        for line in lines:
            tmp = line.strip()
            if not tmp:
                ret.append(line.strip())
        return ret


class StrictLineFC(LineFC):

    def __init__(self, src: str, dst: str):
        super(StrictLineFC, self).__init__(src, dst, ignore=0)


class IgnoreBEBlankLineFC(LineFC):

    def __init__(self, src: str, dst: str):
        super(IgnoreBEBlankLineFC, self).__init__(src, dst, ignore=1)


class IgnoreAllBlankLineFC(LineFC):

    def __init__(self, src: str, dst: str):
        super(IgnoreAllBlankLineFC, self).__init__(src, dst, ignore=2)


class IgnoreAllBlankLineAndBESpaceFC(LineFC):

    def __init__(self, src: str, dst: str):
        super(IgnoreAllBlankLineAndBESpaceFC, self).__init__(src, dst, ignore=3)
