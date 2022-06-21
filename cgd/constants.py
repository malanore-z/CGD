from enum import Enum


class Lang(Enum):

    UNKNOWN = "unknown"
    C = "c"
    CPP = "cpp"
    JAVA = "java"
    PY = "py"


DEFAULT_ARGS = {
    Lang.C: ["-O2", "-g", "-Wall", "-std=c++11"],
    Lang.CPP: ["-O2", "-g", "-Wall", "-std=c++11"],
    Lang.JAVA: [],
    Lang.PY: []
}
