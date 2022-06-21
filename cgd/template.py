import os
import shutil


README = """#

+ Time Limit: 1s
+ Memory Limit: 256MB

## Description

## Input

## Output

## Sample Input 1

```text
```

## Sample Output 1

```text
```

## Hint

"""

MAIN_CPP = """#include <iostream>
#include <string>
#include <cstring>
#include <vector>
#include <algorithm>

using namespace std;

int main() {
    ios::sync_with_stdio(false);

    return 0;
}
"""

MAIN_JAVA = """import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        
    }
}
"""

MAIN_PY = """import math


if __name__ == "__main__":
    pass

"""

GEN_PY = """import typing
from dataclasses import dataclass

from cgd import BaseSample, BaseGenerator


@dataclass
class Sample(BaseSample):
    
    pass


class Generator(BaseGenerator):
    
    def __init__(self):
        super(Generator, self).__init__()
        self.fixed_samples = []
        self.rand_args = []
        
    def _generate(self, *args, **kwargs) -> typing.Tuple[BaseSample, BaseSample]:
        pass
        
    def rand(self) -> typing.Tuple[BaseSample, BaseSample]:
        pass

"""


class Template(object):

    def __init__(self, path, clean=False):
        super(Template, self).__init__()
        self.path = path
        if clean and os.path.exists(self.path):
            shutil.rmtree(self.path)

    def generate(self):
        os.makedirs(self.path, exist_ok=True)

        with open(os.path.join(self.path, "problem.md"), "w") as f:
            f.write(README)

        with open(os.path.join(self.path, "main.cpp"), "w") as f:
            f.write(MAIN_CPP)

        with open(os.path.join(self.path, "Main.java"), "w") as f:
            f.write(MAIN_JAVA)

        with open(os.path.join(self.path, "main.py"), "w") as f:
            f.write(MAIN_PY)

        with open(os.path.join(self.path, "gen.py"), "w") as f:
            f.write(GEN_PY)
