__all__ = [
    "IntFC"
]


from .fc import FC


class IntReader(object):

    legal_chars = "-0123456789"

    def __init__(self, f):
        super(IntReader, self).__init__()
        self.f = f
        self.line = ""
        self.pos = 0

    def next_int(self):
        while True:
            if self.pos >= len(self.line):
                self.line = self.f.readline()
                self.pos = 0
                if not self.line:
                    return None
            new_int = False
            while self.pos < len(self.line):
                if self.line[self.pos] in self.legal_chars:
                    new_int = True
                    break
                self.pos += 1
            if new_int:
                break

        neg = 0
        if self.line[self.pos] == '-':
            neg += 1
        self.pos += neg
        v = 0
        while self.pos < len(self.line):
            if self.line[self.pos] not in self.legal_chars:
                break
            v = 10 * v + (ord(self.line[self.pos]) - ord('0'))
            self.pos += 1
        if neg == 1:
            v = -v
        return v


class IntFC(FC):

    def compare(self) -> bool:
        with open(self.src, "r") as src_f, open(self.dst, "r") as dst_f:
            src_ir = IntReader(src_f)
            dst_ir = IntReader(dst_f)
            while True:
                src_v = src_ir.next_int()
                dst_v = dst_ir.next_int()
                if src_v is None and dst_v is None:
                    break
                if src_v is None:
                    self._src_line = "EOF"
                    self._dst_line = str(dst_v)
                    return False
                if dst_v is None:
                    self._src_line = str(src_v)
                    self._dst_line = "EOF"
                    return False
                if src_v != dst_v:
                    self._src_line = str(src_v)
                    self._dst_line = str(dst_v)
                    return False
        return True
